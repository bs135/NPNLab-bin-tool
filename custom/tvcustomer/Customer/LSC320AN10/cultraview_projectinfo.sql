DROP TABLE IF EXISTS "android_metadata";
CREATE TABLE android_metadata (locale TEXT);
INSERT INTO "android_metadata" VALUES('zh_CN');
DROP TABLE IF EXISTS "tbl_SoftwareVersion";
CREATE TABLE [tbl_SoftwareVersion] (
[id] INTEGER  NOT NULL PRIMARY KEY,
[MainVersion] TEXT  NULL,
[ModelName] TEXT NULL,
[DeviceName] TEXT NULL,
[PanelName] TEXT NULL,
[CustomVersion] TEXT NULL,
[Country] TEXT NULL,
[MovementVer] TEXT NULL,
[OrderID] TEXT NULL
);
INSERT INTO "tbl_SoftwareVersion" VALUES(1,'VNN-CV358H_B42-V033','SmartTV','SmartTV','LSC320AN10','V033','EUROPE','XXXX','80000001');

DROP TABLE IF EXISTS "tbl_Configuration";
CREATE TABLE [tbl_Configuration] (
[id] INTEGER  NOT NULL PRIMARY KEY,
[BootLoader] TEXT NULL,
[GuideMode] TEXT NULL,
[FreeOrCharge] TEXT NULL,
[Theme] TEXT NULL,
[Enable3D] TEXT NULL,
[EnableCEC] TEXT NULL,
[EnableMHL] TEXT NULL,
[EnableSPDIF] TEXT NULL,
[EnableATV] TEXT NULL,
[EnableDTV] TEXT NULL,
[EnableAD] TEXT NULL,
[EnableSurround] TEXT NULL,
[EnableARC] TEXT NULL,
[EnableStoreMode] TEXT NULL,
[EnableDolby] TEXT NULL,
[EnableWifiAP] TEXT NULL,
[EnableBluetooth] TEXT NULL,
[EnableCIInfo] TEXT NULL,
[EnableSMRecovery] TEXT NULL,
[TenCurveVolume] TEXT NULL,
[OEMFactory] TEXT NULL
);
INSERT INTO "tbl_Configuration" VALUES(1, "3", "1", "CHARGE", "DEFAULT", "0", "1", "0", "1", "1", "1", "1", "1","1","0","1","1","1","1","1","1","0");

DROP TABLE IF EXISTS "tbl_Languageselect";
CREATE TABLE [tbl_Languageselect] (
[language] TEXT  NULL,
[flag] INTEGER  NULL
);
INSERT INTO "tbl_Languageselect" VALUES("en_US",1);
INSERT INTO "tbl_Languageselect" VALUES("zh_CN",1);
INSERT INTO "tbl_Languageselect" VALUES("zh_TW",0);
INSERT INTO "tbl_Languageselect" VALUES("de_DE",0);
INSERT INTO "tbl_Languageselect" VALUES("fr_FR",0);
INSERT INTO "tbl_Languageselect" VALUES("it_IT",0);
INSERT INTO "tbl_Languageselect" VALUES("es_ES",0);
INSERT INTO "tbl_Languageselect" VALUES("cs_CZ",0);
INSERT INTO "tbl_Languageselect" VALUES("da_DK",0);
INSERT INTO "tbl_Languageselect" VALUES("el_GR",0);
INSERT INTO "tbl_Languageselect" VALUES("hu_HU",0);
INSERT INTO "tbl_Languageselect" VALUES("nl_NL",0);
INSERT INTO "tbl_Languageselect" VALUES("nb_NO",0);
INSERT INTO "tbl_Languageselect" VALUES("pl_PL",0);
INSERT INTO "tbl_Languageselect" VALUES("pt_PT",0);
INSERT INTO "tbl_Languageselect" VALUES("ru_RU",1);
INSERT INTO "tbl_Languageselect" VALUES("ro_RO",0);
INSERT INTO "tbl_Languageselect" VALUES("sr_RS",0);
INSERT INTO "tbl_Languageselect" VALUES("fi_FI",0);
INSERT INTO "tbl_Languageselect" VALUES("sv_SE",0);
INSERT INTO "tbl_Languageselect" VALUES("bg_BG",0);
INSERT INTO "tbl_Languageselect" VALUES("sk_SK",0);
INSERT INTO "tbl_Languageselect" VALUES("ar_MA",0);
INSERT INTO "tbl_Languageselect" VALUES("tr_TR",0);
INSERT INTO "tbl_Languageselect" VALUES("iw_IL",0);
INSERT INTO "tbl_Languageselect" VALUES("ko_KR",0);
INSERT INTO "tbl_Languageselect" VALUES("fa_IR",0);
INSERT INTO "tbl_Languageselect" VALUES("th_TH",0);
INSERT INTO "tbl_Languageselect" VALUES("vi_VN",1);
INSERT INTO "tbl_Languageselect" VALUES("mn_MN",0);
INSERT INTO "tbl_Languageselect" VALUES("uk_UA",0);
INSERT INTO "tbl_Languageselect" VALUES("in_ID",0);
