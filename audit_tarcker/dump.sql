BEGIN TRANSACTION;
CREATE TABLE Audit_report (Audit_id varchar(20) primary key, auditor_name varchar(20) not null, planned_date DATE not null, state varchar(20) not null, city varchar(20) not null, client_name varchar(20) not null, auditor_contact BIGINT not null, audit_status varchar(20) not null, payment_amount numeric not null, payment_status varchar(20) not null);
INSERT INTO "Audit_report" VALUES('AA0001','RAJESH','2025-01-01','TELANGANA','VIKARBAD','AJAY&GROUPS',7678738098,'Pending','900','Pending');
INSERT INTO "Audit_report" VALUES('AA0002','RAGHAVENDHAR','2025-01-01','TELANGANA','HYDERBAD','TAXSOLUTIONS',7678738099,'Completed','1000','Pending');
INSERT INTO "Audit_report" VALUES('AA0003','SOMESH','2025-01-01','KARNATAKA','BENGULURU','AAKKA',7678738100,'Pending','1200','Paid');
INSERT INTO "Audit_report" VALUES('AA0004','RAMESH','2025-01-01','TELANGANA','VIKARBAD','COST&COUNT',7678738101,'Pending','800','Pending');
INSERT INTO "Audit_report" VALUES('AA0005','ARVI','2025-01-01','TELANGANA','HYDERBAD','AJAY&GROUPS',7678738102,'In Progress','950','Pending');
CREATE TABLE Auditor_data (Auditor_Id varchar(20) primary key , auditor_name varchar(20) not null , number_of_audits BIGINT , review json );
DELETE FROM "sqlite_sequence";
COMMIT;
