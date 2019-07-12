from django.contrib.gis import admin
from named_storms.models import (
    NamedStorm, CoveredData, CoveredDataProvider, NamedStormCoveredData, NSEM,
    NamedStormCoveredDataLog, NsemPsaData,
    NsemPsaVariable)


class CoveredDataInline(admin.TabularInline):
    model = NamedStorm.covered_data.through
    show_change_link = True
    extra = 0
    exclude = ('geo',)  # editing an inline geometry isn't straight forward

    def has_add_permission(self, request):
        # disabled since we can't edit geo which is a required field
        return False


class NamedStormCoveredDataProviderInline(admin.TabularInline):
    model = CoveredDataProvider
    show_change_link = True
    extra = 0


class NsemPsaVariableInline(admin.TabularInline):
    model = NsemPsaVariable
    show_change_link = True
    extra = 0
    fields = ('nsem', 'name', 'data_type')

    def has_add_permission(self, request):
        # disabled since we can't edit geo which is a required field
        return False


@admin.register(NamedStorm)
class NamedStormInlineAdmin(admin.GeoModelAdmin):
    inlines = (
        CoveredDataInline,
    )
    list_display = ('name', 'date_start', 'date_end', 'active',)
    list_filter = ('name', 'date_start', 'date_end', 'active',)


@admin.register(CoveredData)
class CoveredDataAdmin(admin.GeoModelAdmin):
    list_display = ('id', 'name', 'active', 'url',)
    inlines = (
        NamedStormCoveredDataProviderInline,
    )


@admin.register(CoveredDataProvider)
class CoveredDataProviderAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'covered_data', 'active', 'url', 'processor_factory', 'processor_source', 'epoch_datetime',)
    list_filter = ('active',)


@admin.register(NamedStormCoveredData)
class NamedStormCoveredDataAdmin(admin.GeoModelAdmin):
    list_display = ('named_storm', 'covered_data', 'date_start', 'date_end')
    list_filter = ('named_storm', 'covered_data', 'date_start', 'date_end')


@admin.register(NSEM)
class NSEMAdmin(admin.GeoModelAdmin):
    list_display = ('id', 'named_storm', 'date_requested', 'date_returned', 'covered_data_snapshot', 'model_output_snapshot',)
    list_filter = ('named_storm', 'date_requested', 'date_returned',)
    readonly_fields = ('date_requested',)
    inlines = (NsemPsaVariableInline,)


@admin.register(NsemPsaVariable)
class NsemPsaVariableAdmin(admin.GeoModelAdmin):
    list_display = ('id', 'nsem', 'name', 'data_type')


@admin.register(NsemPsaData)
class NsemPsaDataAdmin(admin.GeoModelAdmin):
    list_display = ('nsem_psa_variable', 'value', 'date')
    list_filter = ('nsem_psa_variable',)


@admin.register(NamedStormCoveredDataLog)
class DataLogAdmin(admin.ModelAdmin):
    list_display = ('named_storm', 'covered_data', 'date', 'success', 'snapshot',)
    list_filter = ('named_storm', 'covered_data', 'date', 'success',)
    readonly_fields = ('date',)  # hidden by default since it uses auto_now_add
