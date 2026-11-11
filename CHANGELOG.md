# Changelog / История версий

История версий сборки **MHI2-Carplay-Maps 790** (Škoda MU1440 + приборка 790).
Формат — [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/). Версии — `790 vN`, теги в git — `790-vN`.
История оригинального проекта omonob — в [README.omonob.md](README.omonob.md) и [releases/](releases/).

<!--
Шаблон для новой версии (скопировать над последней версией и заполнить):

## [790 vN] — ГГГГ-ММ-ДД

База: omonob/MHI2-Carplay-Maps vX.Y.Z

### Добавлено
- 

### Изменено
- 

### Исправлено
- 

### Удалено
- 

Проверено на: машина / train / MU / приборка / iPhone, iOS / навигаторы
SHA-256 архива: 
-->

## [Не выпущено]

—

## [790 v2] — 2026-11-11

База: omonob/MHI2-Carplay-Maps **v2.0.1** (вместо 1.2.2).

### Добавлено
- Всё из omonob 2.0.1: страница Virtual Cockpit settings в App-Connect, карточка Left / Right / Center / Off с автоматической сменой зоны, Mirroring, ограничение логов и освобождение видеобуфера.
- Вариант **YANDEX-2026** (по умолчанию): зоны под Яндекс Карты, подобранные в машине; время прибытия при карточке Left и Right; 30 кадров/с.
- Схемы зон обоих вариантов (`skoda-mu1440-790/docs/zones/`).

### Изменено
- Меню `cpmap-790-variants`: два варианта — YANDEX-2026 и OMONOB 2.0.1 classic (оригинал побайтно) — и Show.
- Show показывает вариант, сторону карточки и заполненность RAM-диска.
- Сборка вариантов: `tools/gen_core201.py` (правка только данных `core.so` omonob 2.0.1, места находятся по шаблону).

### Удалено
- Варианты v1 (YANDEX11–55, GOOGLE11–22, OMONOB 1.2.2) и их кнопки — установщик удаляет их из меню.
- `libcardshim.so` и `CLUSTER_ZOOM`: в omonob 2.0.1 не нужны.
- Свой переключатель RAM-логов и `carplay-cluster-supervisor.nolog`: логи как в omonob 2.0.1, он сам ограничивает их размер.

Проверено на: Škoda Octavia A7 / `MHI2_ER_SKG13_P4526_1` / MU1440 / `5E0 920 790 A` / iPhone по кабелю, iOS 27 / Яндекс Карты.
SHA-256 архива `MHI2-Carplay-Maps-790-v2.zip`: `fbcc1b5086783b9d021e82f2ae7254631317ef0d19b296b244455f25d17be00d`

## [790 v1] — 2026-10-27

База: omonob/MHI2-Carplay-Maps **v1.2.2**.

### Добавлено
- Карточка манёвра на приборке 790: адрес экрана приборки `maps:/car/instrumentcluster` вместо `…/map`.
- Время прибытия на приборке (`showETA=yes`) в вариантах YANDEX11–44 и GOOGLE11–22.
- Карточка сверху полосой (`maneuverLayout=topAligned`) — вариант YANDEX55.
- 8 вариантов с переключением из MQB Toolbox (меню `cpmap-790-variants`): OMONOB 1.2.2 classic, YANDEX11 (по умолчанию), YANDEX22, YANDEX33, YANDEX44, YANDEX55, GOOGLE11, GOOGLE22.
- `libcardshim.so` (mathsls, GPL-3.0): дисплей объявляется iPhone как Instrument Cluster, стиль карточки `CLUSTER_ZOOM=1.5`.
- Переключатель RAM-логов (OFF/ON) для любого варианта. **Show** показывает заполненность RAM-диска в %.
- Скрипты воспроизводимой сборки (`skoda-mu1440-790/tools/`) и список изменений (`skoda-mu1440-790/CHANGES.md`).

### Изменено
- Частота кадров 30 во всех вариантах, кроме OMONOB (40, как в оригинале).
- Безопасные зоны подобраны под Яндекс и Google, курсор выше, чем в оригинале.
- Install 790 сразу ставит вариант YANDEX11 и выключает RAM-логи.

### Исправлено
- RAM-диск больше не переполняется логами мода при долгой езде (по умолчанию логи идут в `/dev/null`).

Проверено на: Škoda Octavia A7 / `MHI2_ER_SKG13_P4526_1` / MU1440 / `5E0 920 790 A` / iPhone по кабелю, iOS 27 / Яндекс Навигатор, Google Maps, Amap, Apple Карты.
SHA-256 архива `MHI2-Carplay-Maps-790-v1.zip`: `fd7b84acbc963e7d21a714ad322481835381ec208d594e838fde8e690657e34b`

[Не выпущено]: https://github.com/sli25555-spec/MHI2-Carplay-Maps-790/compare/790-v2...HEAD
[790 v2]: https://github.com/sli25555-spec/MHI2-Carplay-Maps-790/releases/tag/790-v2
[790 v1]: https://github.com/sli25555-spec/MHI2-Carplay-Maps-790/releases/tag/790-v1
