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
  DelLink text DEFAULT "off",
  cPubInfo text DEFAULT "on",
  cFan text DEFAULT "off",
  cRel text DEFAULT "off",
  cCh text DEFAULT "off",
  cAddTags text DEFAULT "off",
  cSumm text DEFAULT "on",
  cSumLength integer DEFAULT "700",
  DelUpdate text DEFAULT "off",
  DelErr text DEFAULT "off",
  DelChapter text DEFAULT "off",
  Image text DEFAULT "on",
  Num text DEFAULT ","
);
