# Generated by Django 3.2.4 on 2021-09-06 07:44

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('m3_gar', '0002_auto_20210707_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddhouseTypes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('shortname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Краткое наименование')),
                ('desc', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('updatedate', models.DateField(verbose_name='Дата внесения (обновления) записи')),
                ('startdate', models.DateField(verbose_name='Начало действия записи')),
                ('enddate', models.DateField(verbose_name='Окончание действия записи')),
                ('isactive', models.BooleanField(verbose_name='Статус активности')),
            ],
            options={
                'verbose_name': 'Тип дома',
                'verbose_name_plural': 'Типы домов',
            },
        ),
        migrations.AddField(
            model_name='addrobj',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addrobjdivision',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admhierarchy',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apartments',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carplaces',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='changehistory',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='houses',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='munhierarchy',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='normativedocs',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='param',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reestrobjects',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rooms',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='steads',
            name='region_code',
            field=models.SmallIntegerField(default=0, verbose_name='Код региона'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addrobj',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор адресного объекта типа INTEGER'),
        ),
        migrations.AlterField(
            model_name='addrobj',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Статус действия над записью – причина появления записи'),
        ),
        migrations.AlterField(
            model_name='addrobjdivision',
            name='childid',
            field=models.ForeignKey(db_column='childid', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Дочерний ID'),
        ),
        migrations.AlterField(
            model_name='addrobjdivision',
            name='parentid',
            field=models.ForeignKey(db_column='parentid', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Родительский ID'),
        ),
        migrations.AlterField(
            model_name='admhierarchy',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор объекта'),
        ),
        migrations.AlterField(
            model_name='admhierarchy',
            name='parentobjid',
            field=models.ForeignKey(blank=True, db_column='parentobjid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Идентификатор родительского объекта'),
        ),
        migrations.AlterField(
            model_name='apartments',
            name='aparttype',
            field=models.ForeignKey(blank=True, db_column='aparttype', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.apartmenttypes', verbose_name='Тип комнаты'),
        ),
        migrations.AlterField(
            model_name='apartments',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор объекта типа INTEGER'),
        ),
        migrations.AlterField(
            model_name='apartments',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Статус действия над записью – причина появления записи'),
        ),
        migrations.AlterField(
            model_name='carplaces',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор объекта типа INTEGER'),
        ),
        migrations.AlterField(
            model_name='carplaces',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Статус действия над записью – причина появления записи'),
        ),
        migrations.AlterField(
            model_name='changehistory',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Тип операции'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='housetype',
            field=models.ForeignKey(blank=True, db_column='housetype', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.housetypes', verbose_name='Основной тип дома'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор объекта типа INTEGER'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Статус действия над записью – причина появления записи'),
        ),
        migrations.AlterField(
            model_name='munhierarchy',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор адресного объекта '),
        ),
        migrations.AlterField(
            model_name='munhierarchy',
            name='parentobjid',
            field=models.ForeignKey(blank=True, db_column='parentobjid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Идентификатор родительского объекта'),
        ),
        migrations.AlterField(
            model_name='normativedocs',
            name='kind',
            field=models.ForeignKey(db_column='kind', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.normativedocskinds', verbose_name='Вид документа'),
        ),
        migrations.AlterField(
            model_name='normativedocs',
            name='type',
            field=models.ForeignKey(db_column='type', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.normativedocstypes', verbose_name='Тип документа'),
        ),
        migrations.AlterField(
            model_name='param',
            name='typeid',
            field=models.ForeignKey(db_column='typeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.paramtypes', verbose_name='Тип параметра'),
        ),
        migrations.AlterField(
            model_name='reestrobjects',
            name='levelid',
            field=models.ForeignKey(db_column='levelid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.objectlevels', verbose_name='Уровень объекта'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор объекта типа INTEGER'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Статус действия над записью – причина появления записи'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='roomtype',
            field=models.ForeignKey(blank=True, db_column='roomtype', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.roomtypes', verbose_name='Тип комнаты или офиса'),
        ),
        migrations.AlterField(
            model_name='steads',
            name='objectid',
            field=models.ForeignKey(db_column='objectid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.reestrobjects', verbose_name='Глобальный уникальный идентификатор объекта типа INTEGER'),
        ),
        migrations.AlterField(
            model_name='steads',
            name='opertypeid',
            field=models.ForeignKey(db_column='opertypeid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.operationtypes', verbose_name='Статус действия над записью – причина появления записи'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='addtype1',
            field=models.ForeignKey(blank=True, db_column='addtype1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.addhousetypes', verbose_name='Дополнительный тип дома 1'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='addtype2',
            field=models.ForeignKey(blank=True, db_column='addtype2', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='m3_gar.addhousetypes', verbose_name='Дополнительный тип дома 2'),
        ),
    ]
