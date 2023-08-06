-- {{ hostname }};
-- role: {{ designated_role }};
!db2start;
{{ db2_backres_cmd }};
CONNECT TO {{ db_name }};
{{ db2_hadr_cfg }};
FORCE APPLICATIONS ALL;
DEACTIVATE DB {{ db_name }};
ACTIVATE DB {{ db_name }};
!db2stop;
!db2start;
ACTIVATE DB {{ db_name }};
{{ db2_hadr_start_cmd }};
!{{ db2_audit_cmd }};
UPDATE ALTERNATE SERVER FOR DATABASE {{ db_name }} USING HOSTNAME {{ db2_acr_host }} PORT {{ db2_acr_port }};


