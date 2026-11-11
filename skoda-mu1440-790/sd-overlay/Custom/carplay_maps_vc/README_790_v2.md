# MHI2-Carplay-Maps 790 v2

Unofficial modification of omonob/MHI2-Carplay-Maps **v2.0.1** (GPL-3.0) for Škoda Columbus MHI2 **MU1440** with the **790** virtual cockpit (AID 10.25"). Not affiliated with or endorsed by omonob.

## English

**Adds to omonob 2.0.1:** arrival time (ETA) with the Left and Right card, a zone set tuned for Yandex Maps (YANDEX-2026), 30 fps, a variant menu in MQB Toolbox. Everything else is omonob 2.0.1 unchanged: the Virtual Cockpit settings page, Mirroring, automatic zone switching, logging and video-buffer handling.

**Install**
1. Back up the unit. **Disconnect CarPlay** (unplug the cable).
2. Extract the ZIP to the SD-card root.
3. MQB Toolbox → Customization → CarPlay Maps VC → **Install AID 10.5**. Wait for `CPMAP_INSTALL_OK`, then do a full reboot (hold the power button ~10 s).
4. App-Connect settings → Virtual Cockpit settings → Navigation card → **Left** or **Right**.

Default variant: YANDEX-2026. Switch in CarPlay Maps VC → **cpmap-790-variants** (keep the SD card in, reboot after switching). Undo: **Restore factory files**.

Variants: **YANDEX-2026** (default; card + ETA, 30 fps) and **OMONOB 2.0.1 classic** (unchanged). Zones: `VARIANTS.txt`. Changes: `CHANGES.md`.

## Русский

**Что добавлено к omonob 2.0.1:** время прибытия при карточке Left и Right, зоны под Яндекс Карты (YANDEX-2026), 30 кадров/с, меню вариантов в MQB Toolbox. Всё остальное — omonob 2.0.1 без изменений: страница Virtual Cockpit settings, Mirroring, автоматическая смена зон, логи и видеобуфер.

**Установка**
1. Бэкап. **Отключите CarPlay** (выньте кабель).
2. Распакуйте ZIP в корень SD-карты.
3. MQB Toolbox → Customization → CarPlay Maps VC → **Install AID 10.5**. Дождитесь `CPMAP_INSTALL_OK` и сделайте полную перезагрузку (кнопка питания ~10 с).
4. Настройки App-Connect → Virtual Cockpit settings → Navigation card → **Left** или **Right**.

По умолчанию вариант YANDEX-2026. Переключение: CarPlay Maps VC → **cpmap-790-variants** (SD-карта в магнитоле, после переключения перезагрузка). Откат: **Restore factory files**.

Варианты: **YANDEX-2026** (по умолчанию; карточка + время прибытия, 30 кадров/с) и **OMONOB 2.0.1 classic** (без изменений). Зоны: `VARIANTS.txt`. Изменения: `CHANGES.md`.
