一、单表查询练习：
 create table salTab(
   eid int primary key auto_increment COMMENT '员工id', 
   dept_id varchar(10) COMMENT '部门id',
   salary double COMMENT '工资',
   offer_time char(6) COMMENT '入职时间',
   level int   COMMENT '员工等级'
 )
 
insert into salTab  values
(null,'1001',300000.00,'201009',0),
(null,'1002',15000.00,'201303',1),
(null,'1002',25000.00,'201208',1),
(null,'1002',19000.00,'201111',1),
(null,'1002',30000.00,'200904',1),
(null,'1003',5000.00,'201409',2),
(null,'1003',6000.00,'201509',2),
(null,'1003',6500.00,'201408',2),
(null,'1003',6500.00,'201409',2),
(null,'1003',7500.00,'201409',2),
(null,'1003',7500.00,'201601',2),
(null,'1003',5500.00,'201509',2),
(null,'1003',8500.00,'201409',2),
(null,'1003',9000.00,'201309',2),
(null,'1003',10000.00,'201209',2),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4000.00,'201609',3),
(null,'1004',4500.00,'201509',3),
(null,'1004',4500.00,'201509',3),
(null,'1004',4500.00,'201509',3),
(null,'1004',4500.00,'201509',3),
(null,'1004',4500.00,'201509',3),
(null,'1004',4500.00,'201509',3),
(null,'1004',3000.00,'201509',3),
(null,'1004',3000.00,'201509',3),
(null,'1004',3000.00,'201509',3),
(null,'1004',3000.00,'201509',3),
(null,'1004',2500.00,'201612',3),
(null,'1004',2500.00,'201612',3),
(null,'1004',2500.00,'201612',3);

1、查询员工部门id为1001的所有员工
	select * from salTab where dept_id=1001;


2、查询员工工资大于10000的所有员工
	select * from salTab where salary>10000;

3、查询员工工资大于15000且员工等级在(0、1、2)之中的所有员工
	select * from salTab where salary>15000 and level in (0,1,2);

4、查询在201409之前入职的所有员工
	select * from salTab where offer_time<201409

5、查询所有的员工，并按照员工的入职时间排序，先入职的在前
	select * from salTab order by offer_time;

6、统计公司所有员工的平均工资
	select avg(salary) from salTab;

7、统计公司所有员工的工资总和
	selcet sum(salary) as "工资总和" from salTab;

8、统计各个部门的员工平均工资
	select dept_id, avg(salary) from salTab group by dept_id;

9、找出员工平均工资高于20000.00的部门
	select dept_id, avg(salary) from salTab group by dept_id having avg(salary)>20000.00 ;

10、找出公司的最低工资是多少
	select min(salary) from salTab;

11、找出公司的最低工资的员工是谁
	select * from salTab where salary = (select min(salary) from salTab);

	select salary, group_concat(eid) from salTab group by salary limit 1;

12、找出公司的最高工资是多少
	select max(salary) from salTab;


13、找出公司的最高工资的员工是谁
	select * from salTab where salary = (select max(salary) from salTab);

	select salary, group_concat(eid) from salTab group by salary order by salary desc limit 1;

14、找出各个部门的最高工资是多少
	select dept_id, max(salary) from salTab group by dept_id;

	

二、多表查询练习

CREATE TABLE students (
    stu_no      CHAR(4)             PRIMARY KEY     COMMENT '学员id',  
    birth_date  DATE            NOT NULL         	COMMENT '学员生日',
    name  VARCHAR(14)           NOT NULL 			COMMENT '学员的名字',
    gender      ENUM ('M','F')  NOT NULL 			COMMENT '学员性别',    
    enter_date   DATE            NOT NULL 			COMMENT '入学日期'
) COMMENT '学生表';


CREATE TABLE salaries (
    stu_no      CHAR(4)         NOT NULL COMMENT '学生ID',
    salary      double          NOT NULL COMMENT '工资',
    month       INT             NOT NULL COMMENT '发工资月份',
    level       INT             NOT NULL COMMENT '工资等级',
    FOREIGN KEY (stu_no) REFERENCES students (stu_no) ON DELETE CASCADE
) COMMENT '薪资表';

insert into students values
('100','1990-08-19','JACK','M','20160811'),
('101','1970-08-12','TOM','M','20100606'),
('102','1996-03-19','JAMES','M','20140101'),
('103','1987-04-28','KETTY','F','20130910'),
('104','1983-05-19','JIM','F','20160418');

insert  into `salaries`(`stu_no`,`salary`,`month`,`level`) 
values (100,12000,201601,2),
(101,9000,201601,1),
(102,13000,201601,3),
(103,8300,201601,1),
(104,9500,201601,1),
(100,12200,201602,2),
(101,9200,201602,1),
(102,13200,201602,3),
(103,8500,201602,1),
(104,9700,201602,1),
(100,12400,201603,2),
(101,9400,201603,1),
(102,13400,201603,3),
(103,8700,201603,1),
(104,9900,201603,1),
(100,12600,201604,2),
(101,9600,201604,1),
(102,13600,201604,3),
(103,8900,201604,1),
(104,10100,201604,1),
(100,12800,201605,2),
(101,9800,201605,1),
(102,13800,201605,3),
(103,9100,201605,1),
(104,10300,201605,1),
(100,12800,201606,2),
(101,9800,201606,1),
(102,13800,201606,3),
(103,9100,201606,1),
(104,10300,201606,1),
(100,13000,201607,2),
(101,10000,201607,1),
(102,14000,201607,3),
(103,9300,201607,1),
(104,10500,201607,1),
(100,13200,201608,2),
(101,10200,201608,1),
(102,14200,201608,3),
(103,9500,201608,1),
(104,10700,201608,1),
(100,13400,201609,2),
(101,10400,201609,1),
(102,14400,201609,3),
(103,9700,201609,1),
(104,10900,201609,1),
(100,13600,201610,2),
(101,10600,201610,1),
(102,14600,201610,3),
(103,9900,201610,1),
(104,11100,201610,1),
(100,13800,201611,2),
(101,10800,201611,1),
(102,14800,201611,3),
(103,10100,201611,1),
(104,11300,201611,1),
(100,14000,201612,2),
(101,11000,201612,1),
(102,15000,201612,3),
(103,10300,201612,1),
(104,11500,201612,1);


-- 1、查看学生总数(students)
	select count(stu_no) from students; 


-- 2、查询学员JAMES的每个月都发了多少工资(students、salaries)
	-- select * from salaries where stu_no = (select stu_no from students where students.name="JAMES");

	select stu.name, sal.salary, sal.month from students as stu left join salaries as sal on stu.stu_no=sal.stu_no and stu.name="JAMES";

	

-- 3、查询学员JAMES在201602月发了多少工资(students、salaries)

	-- select * from salaries where stu_no = (select stu_no from students where students.name="JAMES") and month="201602";

	select stu.name, sal.salary, sal.month from students as stu inner join salaries as sal on stu.stu_no=sal.stu_no and stu.name="JAMES" and sal.month="201602";



-- 4、查询学员JAMES的2016年年薪(students、salaries)

	-- select sum(salary) from salaries where stu_no = (select stu_no from students where students.name="JAMES");

	select stu.name, sum(sal.salary) from students as stu inner join salaries as sal on stu.stu_no=sal.stu_no and stu.name="JAMES" and sal.month like "2016%";



-- 5、查询学员JAMES的月平均工资(students、salaries)

	-- select avg(salary) from salaries where stu_no = (select stu_no from students where students.name="JAMES");

	select stu.name, round(avg(sal.salary),2) from students as stu inner join salaries as sal on stu.stu_no=sal.stu_no and stu.name="JAMES";
