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

Проверено на: Škoda Octavia A7 / `MHI2_ER_SKG13_P4526_1` / MU1440 / `5E0 920 790 A` / iPhone по кабелю, iOS 27 / Яндекс, Google Maps, Amap.
SHA-256 архива `MHI2-Carplay-Maps-790-v1.zip`: `fd7b84acbc963e7d21a714ad322481835381ec208d594e838fde8e690657e34b`

[Не выпущено]: https://github.com/sli25555-spec/MHI2-Carplay-Maps-790/compare/790-v1...HEAD
[790 v1]: https://github.com/sli25555-spec/MHI2-Carplay-Maps-790/releases/tag/790-v1
