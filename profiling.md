Profiling
=========

Here I describe techniques to measure execution time of code running on a game console.

Game Boy Advance
----------------
Timer use based on snippets posted to the gbadev Discord server by AntonioND [license: CC0]

If code takes less than a quarter frame:
```
REG_TM0CNT_L = 0;
REG_TM0CNT_H = (1 << 7); // TIMER_START if you're using libgba
// Do stuff to be timed
uint16_r cycles = REG_TM0CNT_L;
REG_TM0CNT_H = 0; // Stop timer
```

If code takes a quarter frame or more, use cascade (untested; cascade order may be wrong):
```
REG_TM1CNT_L = 0;
REG_TM1CNT_H = (1 << 7) | (1 << 2);
REG_TM0CNT_L = 0;
REG_TM0CNT_H = (1 << 7);
// Do stuff to be timed
REG_TM0CNT_H = 0; // Stop timer
REG_TM1CNT_H = 0;
uint32_r cycles = ((uint32_t)REG_TM1CNT_L << 16) | (uint32_t)REG_TM0CNT_L;
```
