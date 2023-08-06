!db2cli writecfg add -database {{ db_name }} -host {{ fqdn }} -port {{ db2_ssl_svcename }};
!db2cli writecfg add -dsn {{ db_name }} -database {{ db_name }} -host {{ fqdn }} -port {{ db2_ssl_svcename }};
!db2cli writecfg add -database {{ db_name }} -host {{ fqdn }} -port {{ db2_ssl_svcename }} -parameter "SecurityTransportMode=SSL";
!db2cli writecfg add -database {{ db_name }} -host {{ fqdn }} -port {{ db2_ssl_svcename }} -parameter "SSLClientKeystoredb={{ mgmt_keystore_loc }}";
!db2cli writecfg add -database {{ db_name }} -host {{ fqdn }} -port {{ db2_ssl_svcename }} -parameter "SSLClientKeyStash={{ mgmt_keystore_sth }}";
terminate; 

