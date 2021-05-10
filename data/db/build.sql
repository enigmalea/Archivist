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
