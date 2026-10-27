<div align="center">

# MHI2-Carplay-Maps 790 v1

**CarPlay-карта с карточкой манёвра и временем прибытия на цифровой приборке Škoda (MU1440 + AID 790)**<br>
**CarPlay map with turn card and arrival time on the Škoda virtual cockpit (MU1440 + AID 790)**

[Русский](#русский) · [English](#english) · [Скачать / Download](../../releases/latest)

Неофициальная модификация **[omonob/MHI2-Carplay-Maps](https://github.com/omonob/MHI2-Carplay-Maps) v1.2.2** (GPL-3.0).<br>
Unofficial modification of **omonob/MHI2-Carplay-Maps v1.2.2** (GPL-3.0). Not affiliated with or endorsed by omonob.

</div>

---

<!-- Скриншоты / Screenshots: -->

## Русский

### Что это

Сборка проекта [CarPlay Maps VC](https://github.com/omonob/MHI2-Carplay-Maps) автора **omonob** для одной конкретной связки: **Škoda с магнитолой Columbus MHI2 (MU1440) и цифровой приборкой 790 (AID 10,25")**.

Что добавлено к оригиналу 1.2.2:

- **карточка манёвра** на приборке (стрелка, расстояние, улица): Яндекс Навигатор, Google Maps, Apple Карты, Amap;
- **время прибытия** (`showETA`) под картой;
- **зоны под Яндекс и Google**: курсор выше и ближе к центру, карточка у края;
- **30 кадров/с** во всех вариантах, кроме оригинального;
- **RAM-логи выключены по умолчанию**, чтобы RAM-диск магнитолы (20 МБ) не переполнялся;
- **меню вариантов** в MQB Toolbox: переключение без переустановки.

### Проверено

| | |
|---|---|
| Машина | Škoda Octavia A7 |
| Магнитола | Columbus MHI2, `MHI2_ER_SKG13_P4526`, MU1440 |
| Приборка | `5E0 920 790 A` (AID 10,25", профиль 790) |
| Телефон | iPhone по кабелю |

Другие машины, прошивки, приборки и беспроводные адаптеры **не проверялись**. Установщик omonob сам откажется работать на неподдерживаемой прошивке.

### Установка

1. Сделайте бэкап: MQB Toolbox → Dump.
2. Скачайте `MHI2-Carplay-Maps-790-v1.zip` из [Releases](../../releases/latest) и распакуйте **в корень** SD-карты (FAT32).
3. MQB Toolbox → mqbcoding → Customization → CarPlay Maps VC → **Install 790 AID 10.5**.
4. Дождитесь `CPMAP_INSTALL_OK` и сделайте полную перезагрузку магнитолы (держать кнопку питания ~10 с).

После установки стоит вариант **YANDEX11**, RAM-логи выключены.

**Откат:** в том же меню **Restore factory files** → `CPMAP_RESTORE_OK` → перезагрузка.

### Варианты

Меню: CarPlay Maps VC → **cpmap-790-variants**. Для переключения SD-карта должна быть в магнитоле, после переключения нужна полная перезагрузка.

| Кнопка | Зона X | Зона Y | FPS | Карточка | Время прибытия |
|---|---|---|---|---|---|
| OMONOB 1.2.2 classic | 202–808 | 16–360 | 40 | нет | нет |
| **YANDEX11** (по умолчанию) | 30–808 | 41–333 | 30 | слева сверху | да |
| YANDEX22 | 65–808 | 41–333 | 30 | слева сверху | да |
| YANDEX33 | 100–850 | 41–333 | 30 | слева сверху | да |
| YANDEX44 | 20–838 | 41–333 | 30 | слева сверху | да |
| YANDEX55 | 100–810 | 41–333 | 30 | сверху полосой | нет |
| GOOGLE11 | 65–808 | 41–351 | 30 | слева сверху | да |
| GOOGLE22 | 45–795 | 41–351 | 30 | слева сверху | да |

**Зона** — область видео приборки (1010×376), внутри которой навигатор ставит курсор, карточку и полосу прибытия. Карта при этом всегда на весь экран.
- карточка висит от левого верхнего угла зоны;
- полоса прибытия — от левого нижнего;
- курсор ставится ближе к низу зоны.

Ещё в меню:
- **RAM logs: OFF / ON** — работает с любым вариантом;
- **Show** — вариант, состояние логов и заполненность RAM-диска в %.

### Известные ограничения

- Размер и цвет карточки выбирают iOS и навигатор: у Яндекса синяя, у Google зелёная, у Amap чёрная.
- Полоса прибытия частично закрывается трапецией с «P» на приборке.
- При карточке сверху (YANDEX55) iOS не показывает полосу прибытия.
- Яндекс не реагирует на масштаб с колёсика руля. Google и Apple Карты реагируют.
- Без маршрута и с маршрутом курсор Яндекса стоит в разных местах.
- `showSpeedLimit` и `showCompass` с Яндексом и Google ничего не показали, поэтому в сборку не вошли.

### Что изменено относительно omonob 1.2.2

Все изменения перечислены в [skoda-mu1440-790/CHANGES.md](skoda-mu1440-790/CHANGES.md). Кратко:

- `core.so` (MU1440/790), правка бинарного файла:
  - безопасная зона;
  - частота кадров;
  - адрес экрана приборки с параметрами `showETA` / `maneuverLayout`.

  Всё воспроизводимо собирается из оригинала скриптом [`tools/build_790_variants.py`](skoda-mu1440-790/tools/build_790_variants.py).
- `libcardshim.so` из [mathsls/MHI2-Carplay-Maps](https://github.com/mathsls/MHI2-Carplay-Maps) (GPL-3.0): дисплей объявляется iPhone как Instrument Cluster. Исходник лежит в [`third_party/mathsls-cardshim`](skoda-mu1440-790/third_party/mathsls-cardshim).
- `carplay-cluster-supervisor.nolog`: путь лога моста заменён на `/dev/null`, способ mathsls. Скрипт: [`tools/patch_supervisor.py`](skoda-mu1440-790/tools/patch_supervisor.py).
- `install-carplay-maps.sh` и `dio_manager.wrapper.sh`: изменения в виде diff лежат в [`patches/`](skoda-mu1440-790/patches).

Остальные файлы релиза побайтно совпадают с полным архивом omonob v1.2.2 (`VW_SKODA_ALL_CarPlay_Maps_VC_FULL_MQB_Toolbox_V4.2A_v1.2.2.zip`).

### Отказ от ответственности

Изменение файлов магнитолы может привести к сбоям загрузки. Используйте на свой риск, на стоящей машине и при стабильном питании. Не настраивайте во время движения.

Škoda, Volkswagen, Apple, CarPlay, Яндекс и Google — товарные знаки своих владельцев и упомянуты только для описания совместимости.

---

## English

**What it is.** A build of omonob's [CarPlay Maps VC](https://github.com/omonob/MHI2-Carplay-Maps) v1.2.2 for one combination: **Škoda Columbus MHI2 (MU1440) with the 790 virtual cockpit (AID 10.25")**.

**What it adds to the original:**
- a **turn card** on the cluster (Yandex Navigator, Google Maps, Apple Maps, Amap);
- an **arrival time** bar (`showETA`);
- safe areas tuned for Yandex and Google;
- **30 fps** in every variant except the original one;
- RAM-disk **logs off by default**;
- a **variant menu** in MQB Toolbox.

**Tested on:** Škoda Octavia A7, `MHI2_ER_SKG13_P4526`, MU1440, cluster `5E0 920 790 A`, iPhone over cable. Nothing else has been tested.

**Install:**
1. Back up the unit.
2. Extract `MHI2-Carplay-Maps-790-v1.zip` from [Releases](../../releases/latest) to the SD-card root.
3. MQB Toolbox → mqbcoding → Customization → CarPlay Maps VC → **Install 790 AID 10.5**.
4. Wait for `CPMAP_INSTALL_OK`, then do a full reboot (hold the power button for about 10 s).

Default variant: YANDEX11, RAM logs off. To undo, use **Restore factory files**.

**Variants:** see the table above. Zone = safe area in the 1010×376 cluster video. The card hangs from the zone's top-left corner and the ETA bar from its bottom-left corner.

**Changes vs omonob 1.2.2:**
- `core.so`: safe area, maxFPS and cluster URL. The long URL is written over two log-only event names, and both URL references (initialURL and `showUI`) point to it. The variants are reproducible with `tools/build_790_variants.py`.
- `libcardshim.so` by mathsls (GPL-3.0), source included.
- Supervisor RAM-log patch by mathsls, reproducible with `tools/patch_supervisor.py`.
- Installer and wrapper changes as diffs in `patches/`.

All other files are byte-identical to omonob's v1.2.2 full MQB package. See [CHANGES.md](skoda-mu1440-790/CHANGES.md).

**Disclaimer.** Modifying head-unit files can cause boot failures. Use at your own risk, with the car parked and on stable power. Trademarks belong to their owners.

---

## Credits / Благодарности

- **[omonob](https://github.com/omonob/MHI2-Carplay-Maps)** — CarPlay Maps VC, the base of this build. The original README is kept as [README.omonob.md](README.omonob.md).
- **[mathsls](https://github.com/mathsls/MHI2-Carplay-Maps)** — libcardshim, the turn-card URL, the RAM-log fix.
- **[perkthefox](https://github.com/perkthefox/mst2-cluster-nav)** — the `showETA` / `maneuverLayout` parameters and research on this cluster (information only, no code used).
- **[chefranov](https://github.com/chefranov/mhi2-au37x-carplay)**, **[kamgurgul](https://github.com/kamgurgul/mhi2_altscreen_carplay)** — information on cluster URL parameters and MU1440 (no code used).
- **jilleb** — [MQB Toolbox](https://github.com/jilleb/mib2-toolbox) (MIT), included in the full SD package.

## License / Лицензия

[GNU GPL v3.0](LICENSE), as the original project. Third-party parts keep their own licenses (mathsls libcardshim: GPL-3.0; MQB Toolbox: MIT).
