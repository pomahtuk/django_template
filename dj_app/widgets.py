#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.db import models
import os
import Image

DEFAULT_LAT = 28.738031
DEFAULT_LNG = 60.713432

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        output = [self.inner_widget.render(name, value, *args, **kwargs)]
        output.append(u'''
<div>
<input type="text" class="vTextField" id="YMapsInput">
<input id="search_btn" value="Найти!" type="button"/>
<div id="YMapsID" style="width: 620px; height: 300px;">
</div>

<script type="text/javascript">
	var map = -1
	var placemark = -1
	var ltt = $('#id_lat');
	var lgg = $('#id_lng');	
	ltt.parent().parent().parent().hide();
	lgg.parent().parent().parent().hide();
	var tv = $('#id_location');
	
	ymaps.ready(init);
	
	function strpos(haystack, needle, offset){
		var i = haystack.indexOf( needle, offset );
		return i >= 0 ? i : false;
	}
	
	function init () {
		var x = tv.val().substr(0, strpos(tv.val(), ",", 0));
		var y = tv.val().substr(strpos(tv.val(), ",", 0)+1, tv.val().length);
		if(!x) x = %f;if(!y) y = %f;
		
		myMap = new ymaps.Map("YMapsID", {
				center: [x, y], // Центр России
				zoom: 14,
				behaviors: ['default', 'scrollZoom', 'drag']
			});
		//myMap.behavior.Drag.enable();
		myMap.controls
			// Кнопка изменения масштаба
			.add('zoomControl')
			// Стандартный набор кнопок
			.add('mapTools');			
			myCollection = new ymaps.GeoObjectCollection();

		myGeoObject = new ymaps.GeoObject({
				 geometry: {
					 type: "Point",
					 coordinates: [x, y]
				 },
				 properties: {
					 iconContent: " ",
					 hintContent: " ",
					 balloonContentHeader: " Точка "
				 }
			 }, {
				 draggable: true,
				 preset: "twirl#blueIcon"
			 });

		myMap.geoObjects.add(myGeoObject);		
		myGeoObject.events.add('dragend', function() {
														tv.val(myGeoObject.geometry._n[0] + ',' + myGeoObject.geometry._n[1]);
														ltt.val(myGeoObject.geometry._n[0]);
														lgg.val(myGeoObject.geometry._n[1]);	
													});		
			
		$('#search_btn').click(function () {
			var search_query = $('#YMapsInput').val();

			ymaps.geocode(search_query, {results: 1}).then(function (res) {
				myCollection="";
				myCollection = res.geoObjects.get(0);			
				myGeoObject = new ymaps.GeoObject({
						 geometry: {
							 type: "Point",
							 coordinates: myCollection.geometry.getCoordinates()
						 },
						 properties: {
							 iconContent: " ",
							 hintContent: myCollection.properties.get('description'),
							 balloonContentHeader: myCollection.properties.get('name')
						 }
					 }, {
						 draggable: true,
						 preset: "twirl#blueIcon"
					 });
				myMap.geoObjects.remove(myGeoObject);				
				myMap.geoObjects.add(myGeoObject);				
				
				myGeoObject.events.add('dragend', function() {
																tv.val(myGeoObject.geometry._n[0] + ',' + myGeoObject.geometry._n[1]);
																ltt.val(myGeoObject.geometry._n[0]);
																lgg.val(myGeoObject.geometry._n[1]);	
															});
				
				myMap.panTo(myGeoObject.geometry.getCoordinates());
				tv.val(myGeoObject.geometry._n[0] + ',' + myGeoObject.geometry._n[1]);
				ltt.val(myGeoObject.geometry._n[0]);
				lgg.val(myGeoObject.geometry._n[1]);				
			});		
			
			return false;
		});		
	}
</script>	
		''' % (DEFAULT_LAT, DEFAULT_LNG))
        return mark_safe(u''.join(output))

    class Media:
        js = (
			'http://api-maps.yandex.ru/2.0/?load=package.full&mode=release&lang=ru-RU&coordorder=longlat',
        )

class LocationFormField(forms.CharField):
    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value

        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)

class LocationField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)