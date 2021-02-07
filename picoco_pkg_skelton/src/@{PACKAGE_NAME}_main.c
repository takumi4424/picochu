#include "pico/stdlib.h"

const uint LED_PIN = 25;

void init()
{
  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);
}

void loop()
{
  gpio_put(LED_PIN, 1);
  sleep_ms(250);
  gpio_put(LED_PIN, 0);
  sleep_ms(250);
}

int main() { init(); while(true) { loop(); } }
