--
-- //          Copyright Amber Whitlock aka enigmalea 2021
-- // Distributed under the Boost Software License, Version 1.0.
-- //    (See accompanying file LICENSE_1_0.txt or copy at
-- //          https://www.boost.org/LICENSE_1_0.txt)

CREATE TABLE IF NOT EXISTS settings (
  GuildID integer PRIMARY KEY,
  Prefix text DEFAULT "$",
  Ign text DEFAULT "%",
  Basic text DEFAULT "on",
  PubInfo text DEFAULT "on",
  Rate text DEFAULT "on",
  Fan text DEFAULT "on",
  Rel text DEFAULT "on",
  Ch text DEFAULT "on",
  AddTags text DEFAULT "on",
  Summ text DEFAULT "on",
  SumLength integer DEFAULT "700",
  DelLink text DEFAULT "off"
);

ALTER TABLE settings ADD COLUMN cPubInfo text DEFAULT "on";
ALTER TABLE settings ADD COLUMN cFan text DEFAULT "off";
ALTER TABLE settings ADD COLUMN cRel text DEFAULT "off";
ALTER TABLE settings ADD COLUMN cCh text DEFAULT "off";
ALTER TABLE settings ADD COLUMN cAddTags text DEFAULT "off";
ALTER TABLE settings ADD COLUMN cSumm text DEFAULT "on";
ALTER TABLE settings ADD COLUMN cSumLength integer DEFAULT "700";
ALTER TABLE settings ADD COLUMN DelUpdate text DEFAULT "off";
ALTER TABLE settings ADD COLUMN DelErr text DEFAULT "off";
ALTER TABLE settings ADD COLUMN DelChapter text DEFAULT "off";
ALTER TABLE settings ADD COLUMN Image text DEFAULT "on";
