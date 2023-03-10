void enable_bdomain_protection(void) {
  register_clear_bits(&(PWR->CR1), PWR_CR1_DBP);
}

void disable_bdomain_protection(void) {
  register_set_bits(&(PWR->CR1), PWR_CR1_DBP);
}

void rtc_init(void){
  uint32_t bdcr_opts = RCC_BDCR_RTCEN;
  uint32_t bdcr_mask = (RCC_BDCR_RTCEN | RCC_BDCR_RTCSEL);
  if (current_board->has_rtc_battery) {
    bdcr_opts |= (RCC_BDCR_LSEDRV_1 |  RCC_BDCR_RTCSEL_0 | RCC_BDCR_LSEON);
    bdcr_mask |= (RCC_BDCR_LSEDRV | RCC_BDCR_LSEBYP | RCC_BDCR_LSEON);
  } else {
    bdcr_opts |= RCC_BDCR_RTCSEL_1;
    RCC->CSR |= RCC_CSR_LSION;
    while((RCC->CSR & RCC_CSR_LSIRDY) == 0){}
  }

  // Initialize RTC module and clock if not done already.
  if((RCC->BDCR & bdcr_mask) != bdcr_opts){
    print("Initializing RTC\n");
    // Reset backup domain
    register_set_bits(&(RCC->BDCR), RCC_BDCR_BDRST);

    // Disable write protection
    disable_bdomain_protection();

    // Clear backup domain reset
    register_clear_bits(&(RCC->BDCR), RCC_BDCR_BDRST);

    // Set RTC options
    register_set(&(RCC->BDCR), bdcr_opts, bdcr_mask);

    // Enable write protection
    enable_bdomain_protection();
  }
}

void rtc_wakeup_init(void) {
  EXTI->IMR1  |=  EXTI_IMR1_IM19;
  EXTI->RTSR1 |=  EXTI_RTSR1_TR19; // rising edge
  EXTI->FTSR1 &=  ~EXTI_FTSR1_TR19; // falling edge

  NVIC_DisableIRQ(RTC_WKUP_IRQn);

  // Disable write protection
  disable_bdomain_protection();
  RTC->WPR = 0xCA;
  RTC->WPR = 0x53;

  RTC->CR &= ~RTC_CR_WUTE;
  while((RTC->ISR & RTC_ISR_WUTWF) == 0){}

  RTC->CR &= ~RTC_CR_WUTIE;
  RTC->ISR &= ~RTC_ISR_WUTF;
  //PWR->CR1 |= PWR_CR1_CWUF;

  RTC->WUTR = DEEPSLEEP_WAKEUP_DELAY;
  // Wakeup timer interrupt enable, wakeup timer enable, select 1Hz rate
  RTC->CR |= RTC_CR_WUTE | RTC_CR_WUTIE | RTC_CR_WUCKSEL_2;

  // Re-enable write protection
  RTC->WPR = 0x00;
  enable_bdomain_protection();

  NVIC_EnableIRQ(RTC_WKUP_IRQn);
}
