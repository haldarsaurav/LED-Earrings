// Rev B concept firmware: ATtiny1616 + LIS2DW12 + 8x10 WS2812-compatible LEDs.
// Compiles with megaTinyCore 2.6.11. Flashing and physical current are unverified.
#include <Arduino.h>
#include <Wire.h>
#include <tinyNeoPixel_Static.h>

constexpr uint8_t WIDTH = 8;
constexpr uint8_t HEIGHT = 10;
constexpr uint8_t LED_COUNT = WIDTH * HEIGHT;
constexpr uint8_t LED_PIN = PIN_PA4;
constexpr uint8_t BUTTON_PIN = PIN_PA6;
constexpr uint8_t VBAT_PIN = PIN_PA5;
constexpr uint8_t SENSOR_ADDR = 0x18;
constexpr bool SERPENTINE = true;
constexpr bool FLIP_VERTICAL = false;
constexpr uint16_t FRAME_MS = 40;                 // 25 frames/s
constexpr uint16_t LOW_BATTERY_MV = 3400;        // revise from cell tests

uint8_t pixelBuffer[LED_COUNT * 3];
tinyNeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB, pixelBuffer);
uint8_t mode = 0;
uint8_t budgetStep = 0;
// Start conservatively with the selected protected 150 mAh cell. These
// brightness estimates still require measured peak and average currents.
const uint8_t channelSumBudget[3] = {10, 16, 24};
bool sensorPresent = false;
bool diagnosticMode = false;
bool batteryLatchedOff = false;
int16_t slopeQ8 = 0;
int16_t slopeSpeed = 0;
uint16_t frameNumber = 0;
uint32_t lastFrame = 0;
uint32_t lowSince = 0;
bool buttonStable = HIGH;
bool buttonRaw = HIGH;
uint32_t buttonChanged = 0;
uint32_t buttonDown = 0;
bool longHandled = false;

uint8_t pixelIndex(uint8_t x, uint8_t y) {
  if (FLIP_VERTICAL) y = HEIGHT - 1 - y;
  if (SERPENTINE && (y & 1)) x = WIDTH - 1 - x;
  return y * WIDTH + x;
}

// Limit the sum of LED channel codes. This only estimates dynamic LED current.
void put(uint8_t x, uint8_t y, uint8_t r, uint8_t g, uint8_t b) {
  const uint16_t sum = (uint16_t)r + g + b;
  const uint8_t limit = channelSumBudget[budgetStep];
  if (sum > limit) {
    r = (uint16_t)r * limit / sum;
    g = (uint16_t)g * limit / sum;
    b = (uint16_t)b * limit / sum;
  }
  strip.setPixelColor(pixelIndex(x, y), r, g, b);
}

bool sensorWrite(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(SENSOR_ADDR);
  Wire.write(reg);
  Wire.write(value);
  return Wire.endTransmission() == 0;
}

bool sensorRead(uint8_t reg, uint8_t *data, uint8_t length) {
  Wire.beginTransmission(SENSOR_ADDR);
  Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(SENSOR_ADDR, length) != length) return false;
  for (uint8_t i = 0; i < length; ++i) data[i] = Wire.read();
  return true;
}

void startSensor() {
  uint8_t id = 0;
  sensorPresent = sensorRead(0x0F, &id, 1) && id == 0x44;
  if (!sensorPresent) return;
  // CTRL2: block-data-update + auto-increment. CTRL1: 50 Hz, LP mode 4.
  sensorPresent = sensorWrite(0x21, 0x0C) && sensorWrite(0x20, 0x43);
}

int16_t readTiltTarget() {
  if (!sensorPresent) {
    // Slow triangular slosh for bench testing without the sensor.
    const uint16_t p = frameNumber % 120;
    return p < 60 ? (int16_t)p * 8 - 240 : 720 - (int16_t)p * 8;
  }
  uint8_t raw[6];
  if (!sensorRead(0x28, raw, 6)) return slopeQ8;
  const int16_t ax = (int16_t)((uint16_t)raw[1] << 8 | raw[0]);
  const int16_t ay = (int16_t)((uint16_t)raw[3] << 8 | raw[2]);
  int32_t denominator = ay;
  if (denominator >= 0 && denominator < 8000) denominator = 8000;
  if (denominator < 0 && denominator > -8000) denominator = -8000;
  // The free surface is perpendicular to gravity: dy/dx = -ax/ay.
  int32_t target = -(int32_t)ax * 256 / denominator;
  if (target > 320) target = 320;
  if (target < -320) target = -320;
  return (int16_t)target;
}

void drawWater() {
  const int16_t target = readTiltTarget();
  // A damped spring makes the surface lag behind a moving earring.
  slopeSpeed += (target - slopeQ8) / 7 - slopeSpeed / 4;
  slopeQ8 += slopeSpeed / 4;
  for (uint8_t x = 0; x < WIDTH; ++x) {
    const int16_t dx2 = (int16_t)x * 2 - (WIDTH - 1);
    const int16_t wave = ((frameNumber + x * 7) % 23 < 5) ? 18 : 0;
    const int16_t surface = 6 * 256 + (slopeQ8 * dx2) / 2 + wave;
    for (uint8_t y = 0; y < HEIGHT; ++y) {
      const int16_t point = (int16_t)y * 256;
      if (point >= surface) put(x, y, 0, 5, 20);
      else if (point + 256 >= surface) put(x, y, 3, 11, 17);
      else put(x, y, 0, 0, 0);
    }
  }
}

void drawHeart() {
  // 8x10 pixel heart with a gentle two-beat pulse.
  static const uint8_t rows[10] = {
    0b00000000, 0b01100110, 0b11111111, 0b11111111, 0b11111111,
    0b01111110, 0b00111100, 0b00011000, 0b00000000, 0b00000000
  };
  const uint8_t phase = frameNumber % 32;
  const uint8_t red = (phase < 3 || (phase >= 7 && phase < 9)) ? 32 : 13;
  for (uint8_t y = 0; y < HEIGHT; ++y)
    for (uint8_t x = 0; x < WIDTH; ++x)
      put(x, y, rows[y] & (0x80 >> x) ? red : 0, 0, 0);
}

void drawSparkle() {
  strip.clear();
  const uint8_t a = (frameNumber * 37) % LED_COUNT;
  const uint8_t b = (frameNumber * 19 + 31) % LED_COUNT;
  strip.setPixelColor(a, 8, 4, 4);
  strip.setPixelColor(b, 3, 6, 7);
}

void drawRainbow() {
  for (uint8_t y = 0; y < HEIGHT; ++y)
    for (uint8_t x = 0; x < WIDTH; ++x) {
      const uint8_t hue = (x * 23 + y * 11 + frameNumber * 2) & 0xFF;
      // A six-sector color wheel, with restrained channel values.
      const uint8_t sector = hue / 43;
      const uint8_t ramp = (hue % 43) / 3;
      const uint8_t r = sector == 0 || sector == 5 ? 14 : (sector == 1 ? 14 - ramp : (sector == 4 ? ramp : 0));
      const uint8_t g = sector == 1 || sector == 2 ? 14 : (sector == 0 ? ramp : (sector == 3 ? 14 - ramp : 0));
      const uint8_t b = sector == 3 || sector == 4 ? 14 : (sector == 2 ? ramp : (sector == 5 ? 14 - ramp : 0));
      put(x, y, r, g, b);
    }
}

// Hold the effect button while switching on to inspect the first pixels,
// sensor response and battery state through the assembled front display.
void drawDiagnostic() {
  strip.clear();
  strip.setPixelColor(pixelIndex(0, 0), 8, 0, 0); // red
  strip.setPixelColor(pixelIndex(1, 0), 0, 8, 0); // green
  strip.setPixelColor(pixelIndex(2, 0), 0, 0, 8); // blue
  for (uint8_t y = 2; y < 6; ++y) {
    if (sensorPresent) strip.setPixelColor(pixelIndex(4, y), 0, 6, 0);
    else strip.setPixelColor(pixelIndex(4, y), 8, 0, 0);
  }
  const uint16_t mv = batteryMillivolts();
  for (uint8_t y = 2; y < 6; ++y) {
    if (mv >= 3700) strip.setPixelColor(pixelIndex(6, y), 0, 6, 0);
    else if (mv >= LOW_BATTERY_MV) strip.setPixelColor(pixelIndex(6, y), 6, 3, 0);
    else strip.setPixelColor(pixelIndex(6, y), 8, 0, 0);
  }
}

void readButton(uint32_t now) {
  const bool raw = digitalRead(BUTTON_PIN);
  if (raw != buttonRaw) { buttonRaw = raw; buttonChanged = now; }
  if (now - buttonChanged > 25 && raw != buttonStable) {
    buttonStable = raw;
    if (raw == LOW) { buttonDown = now; longHandled = false; }
    else if (!longHandled) {
      if (diagnosticMode) diagnosticMode = false;
      else mode = (mode + 1) % 4;
    }
  }
  if (buttonStable == LOW && !longHandled && now - buttonDown > 700) {
    budgetStep = (budgetStep + 1) % 3;
    longHandled = true;
  }
}

uint16_t batteryMillivolts() {
  // Divider: 1 MΩ high + 330 kΩ low. ADC reference assumed to be VDD=3.45 V.
  // 3450 * 1330 / 330 / 1023 = approximately 13.59 mV per 10-bit count.
  const uint16_t adc = analogRead(VBAT_PIN);
  return (uint32_t)adc * 13590UL / 1000UL;
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  diagnosticMode = digitalRead(BUTTON_PIN) == LOW;
  analogReadResolution(10);
  Wire.begin();
  startSensor();
  strip.clear();
  strip.show();
}

void loop() {
  const uint32_t now = millis();
  if (batteryLatchedOff) { delay(1000); return; }
  readButton(now);
  if (now - lastFrame < FRAME_MS) return;
  lastFrame = now;

  // Check roughly once per second; require a sustained low reading.
  if (frameNumber % 25 == 0) {
    if (batteryMillivolts() < LOW_BATTERY_MV) {
      if (lowSince == 0) lowSince = now;
      if (now - lowSince > 3000) {
        batteryLatchedOff = true;
        strip.clear(); strip.show();
        return;
      }
    } else lowSince = 0;
  }

  if (diagnosticMode) drawDiagnostic();
  else switch (mode) {
    case 0: drawWater(); break;
    case 1: drawHeart(); break;
    case 2: drawSparkle(); break;
    default: drawRainbow(); break;
  }
  strip.show();
  ++frameNumber;
}
