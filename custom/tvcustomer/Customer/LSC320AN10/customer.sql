DROP TABLE IF EXISTS "tbl_ATVDefaultPrograms";
CREATE TABLE [tbl_ATVDefaultPrograms] (
[u8CityIndex] INTEGER  NULL,
[u8AtvProgramCount] INTEGER  NULL,
[u8AtvProgramIndex] INTEGER  NULL,
[u32FrequencyKHz] INTEGER  NULL,
[AudioStandard] INTEGER  NULL,
[VideoStandard] INTEGER  NULL,
PRIMARY KEY ([u8CityIndex],[u8AtvProgramIndex])
);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,1,0,83250,2,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,1,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,2,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,3,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,4,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,5,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,6,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,7,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,8,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,9,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,10,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,11,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,12,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,13,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,14,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(0,0,15,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,0,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,1,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,2,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,3,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,4,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,5,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,6,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,7,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,8,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,9,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,10,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,11,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,12,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,13,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,14,0,0,0);
INSERT INTO "tbl_ATVDefaultPrograms" VALUES(1,0,15,0,0,0);
DROP TABLE IF EXISTS "tbl_DTVDefaultPrograms";
CREATE TABLE [tbl_DTVDefaultPrograms] (
[u8CityIndex] INTEGER  NULL,
[u8DtvRouteMode] INTEGER  NULL,
[u8DtvProgramCount] INTEGER  NULL,
[u8DtvProgramIndex] INTEGER  NOT NULL,
[u8RfChNumber] INTEGER  NULL,
[u8QAMMode] INTEGER  NULL,
[u32Frequency] INTEGER  NULL,
[u32SymbolRate] INTEGER  NULL,
[u16TSID] INTEGER  NULL,
[u16ONID] INTEGER  NULL,
[u16NID] INTEGER  NULL,
[u16PCRPID] INTEGER  NULL,
[u16LCN] INTEGER  NULL,
[u16PmtPID] INTEGER  NULL,
[u16ServiceID] INTEGER  NULL,
[u16SourceId] INTEGER  NULL,
[u16VideoPID] INTEGER  NULL,
[u16AudioPID] INTEGER  NULL,
[u8VideoType] INTEGER  NULL,
[u8AudioType] INTEGER  NULL,
[u8NITVersion] INTEGER  NULL,
[u8PATVersion] INTEGER  NULL,
[u8PMTVersion] INTEGER  NULL,
[u8SDTVersion] INTEGER  NULL,
[u8VctVersion] INTEGER  NULL,
[u8RrtVersion] INTEGER  NULL,
PRIMARY KEY ([u8CityIndex],[u8DtvProgramIndex])
);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,0,1,2,474000,6875,1,32766,32766,821,1,820,82,0,821,822,2,1,0,4,5,1,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(0,1,16,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "tbl_DTVDefaultPrograms" VALUES(1,1,16,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
