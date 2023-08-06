create or replace procedure db2inst1.connect_check()
language sql
begin
declare conns bigint default 0;
declare c2 cursor for (select count(*) from table(mon_get_connection(null,-1)) where session_auth_id = SESSION_USER and session_auth_id != 'DB2INST1' and session_auth_id != 'BLUADMIN' and session_auth_id != 'BLUADMIN_MON' and session_auth_id != 'UCMON');
open c2;
fetch c2 into conns;
if (conns > 15) then
signal sqlstate '42502' set message_text='Exceeded maximum limit of 15 connections. Connection refused';
end if;
end@
