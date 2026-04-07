# SAP Service Layer Compatibility Timeline

This document tracks the evolution of the SAP Business One Service Layer and established the verification baseline for the `b1sl` SDK.

## 🏁 Tested Baseline (v0.1.0)
The development and verification of the `v0.1.0` release were performed against:
- **Service Layer Version**: 1.27 (August 2024)
- **SAP Business One Version**: 10.0 FP 2405 (and higher)
- **Protocol**: OData V4 (v2)

---

## 📜 Full Feature Timeline

| Version | Date | Key Changes & Features |
| :--- | :--- | :--- |
| **1.0** | 2014-06-27 | Initial release of SAP Business One Service Layer. |
| **1.1** | 2014-11-11 | Service user, Configuration by request, SessionTimeout, UDO/UDF support. |
| **1.2** | 2014-12-30 | **Support OData version 4**. Metadata for UDF/UDT/UDO. |
| **1.3** | 2015-03-19 | SLD server support, $inlinecount, Service Layer vs DI API samples. |
| **1.4** | 2015-07-20 | Session login/logout, Order preview actions, CORS support. |
| **1.5** | 2015-12-15 | Single Sign-On (SSO). |
| **1.7** | 2016-05-04 | Create Entity with No Content, Aggregation, Attachments. |
| **1.8** | 2016-07-28 | JavaScript Extension, Case-insensitive query, Cross-Joins. |
| **1.9** | 2017-08-14 | Support SAP Business One 9.3 (HANA). |
| **1.11** | 2018-02-09 | Cancel/close entity for UDO, Row level filters. |
| **1.14** | 2019-05-20 | Ping Pong API. |
| **1.15** | 2019-10-20 | Support SAP Business One 10.0 (HANA). Configuration Controller. |
| **1.17** | 2020-01-02 | Support SAP Business One 10.0 PL01 (SQL Server). |
| **1.18** | 2020-04-08 | SQL View support. |
| **1.21** | 2021-03-22 | **Support ETag mechanism**. SQLQueries support for UDO/UDT. |
| **1.22** | 2021-06-10 | Enhanced OData Query ($expand with $select). |
| **1.24** | 2023-07-14 | Update Login/Logout, Permission control for SQL Query. |
| **1.27** | 2024-08-02 | Documentation converted to HTML format. **(SDK Baseline)** |
| **1.28** | 2026-01-07 | Support SAP Business One Webhook. |

## 💡 Important Notes for Developers

### OData Versions
While SAP introduced OData V4 in version 1.2, many older installations still use the v1 (OData V2) endpoint. This SDK defaults to `v2` (OData V4), but you can force `v1` in the client constructor if necessary.

### Concurrency Control (ETags)
If you are using SAP version prior to **1.21**, the ETag features of this SDK (`Optimistic Concurrency`) will not function as they rely on the `If-Match` headers introduced in that version.
