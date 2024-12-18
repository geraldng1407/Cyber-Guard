import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import * as turf from '@turf/turf';

const COUNTRY_BOUNDARIES_URL = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson';

const fetchCountryList = async () => {
    try {
        const response = await fetch('http://localhost:8088/countries');
        if (!response.ok) {
            throw new Error('Failed to fetch country list');
        }
        const countryList = await response.json();
        return countryList;
    } catch (error) {
        console.error('Error fetching country list:', error);
        return [];
    }
};

const fetchCountryData = async (country) => {
    try {
        const response = await fetch(`http://localhost:8088/${country}`);
        if (!response.ok) {
            throw new Error(`Network response was not ok for ${country}`);
        }
        const data = await response.json();
        return { country, ...data };
    } catch (error) {
        console.error(`Error fetching data for ${country}:`, error);
        return { country, "Number of instances flagged": 0, "code": "NA" };
    }
};

const compileCountryData = async (countries) => {
    try {
        const countryDataPromises = countries.map((country) => fetchCountryData(country));
        const compiledData = await Promise.all(countryDataPromises);
        return compiledData;
    } catch (error) {
        console.error('Error compiling country data:', error);
        return [];
    }
};

const mapCountryName = (countryName) => {
    // Map "United States of America" to "United States"
    if (countryName === "United States of America") {
        return "United States";
    }
    return countryName;
};

const mapCountryNameLayer = (countryName) => {
    // Map "United States" to "United States of America"
    if (countryName === "United States") {
        return "United States of America";
    }
    return countryName;
};

const GlobalOverview = () => {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(0);
    const [lat, setLat] = useState(20);
    const [zoom, setZoom] = useState(2);
    const [countryBoundaries, setCountryBoundaries] = useState(null);
    const [countries, setCountries] = useState([]);
    const [trigger, setTrigger] = useState(0);

    const fetchAndUpdateData = () => {
        fetchCountryList().then((fetchedCountries) => {
            setCountries(fetchedCountries);
            compileCountryData(fetchedCountries).then((apiCountryData) => {
                fetch(COUNTRY_BOUNDARIES_URL)
                    .then(response => response.json())
                    .then(data => {
                        const mergedData = {
                            type: 'FeatureCollection',
                            features: data.features.map(feature => {
                                const countryName = mapCountryName(feature.properties.ADMIN);
                                const countryData = apiCountryData.find(
                                    item => countryName === mapCountryName(item.country)
                                );
                                return {
                                    ...feature,
                                    properties: {
                                        ...feature.properties,
                                        ADMIN: countryName,
                                        value: countryData ? countryData['Number of instances flagged'] : 0
                                    }
                                };
                            })
                        };
                        setCountryBoundaries(mergedData);
                        if (map.current && map.current.getSource('country-boundaries')) {
                            map.current.getSource('country-boundaries').setData(mergedData);
                        }
                    })
                    .catch(error => console.error('Error fetching country boundaries:', error));
            });
        });
    };
    

    useEffect(() => {
        fetchAndUpdateData();

        const intervalId = setInterval(() => {
            setTrigger(prev => prev + 1);
        }, 10000);

        return () => clearInterval(intervalId);
    }, []);

    useEffect(() => {
        if (trigger > 0) {
            fetchAndUpdateData();
        }
    }, [trigger]);

    useEffect(() => {
        if (map.current || !countryBoundaries) return;
        mapboxgl.accessToken = 'pk.eyJ1IjoicmVsZWtsYSIsImEiOiJjbTFsMGUybWEwNHlkMnBxdGp1dDJ2ODdtIn0.9tFJfqX72whbkrhIsDM4CA';
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/light-v10',
            center: [lng, lat],
            zoom: zoom,
            projection: 'mercator'
        });

        const popup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false
        });

        map.current.on('load', () => {
            map.current.addSource('country-boundaries', {
                type: 'geojson',
                data: countryBoundaries
            });

            map.current.addLayer({
                id: 'country-choropleth',
                type: 'fill',
                source: 'country-boundaries',
                paint: {
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'value'],
                        0, '#ACE1AF', // Green
                        1, 'rgb(255,165,0)', // Orange
                        2, '#FD5C63' // Red
                    ],
                    'fill-opacity': 0.4
                }
            });

            map.current.on('mousemove', 'country-choropleth', (e) => {
                if (e.features.length > 0) {
                    const feature = e.features[0];
                    map.current.getCanvas().style.cursor = 'pointer';

                    const coordinates = e.lngLat;
                    const countryName = feature.properties.ADMIN
                    const heatmapValue = feature.properties.value || 0;
                    const popupContent = `
                        <h3 style="color: black;">${countryName}</h3>
                        <p style="color: black;">No. of Active Issues: ${heatmapValue.toFixed(2)}</p>
                    `;
                    popup.setLngLat(coordinates).addTo(map.current).setHTML(popupContent);
                }
            });

            map.current.on('mouseleave', 'country-choropleth', () => {
                map.current.getCanvas().style.cursor = '';
                popup.remove();
            });

            map.current.on('click', 'country-choropleth', (e) => {
                if (e.features.length > 0) {
                    const feature = e.features[0];
                    const countryName = feature.properties.ADMIN;
                    window.location.href = `http://localhost:3001/countries/${encodeURIComponent(countryName)}`;
                }
            });

            countryBoundaries.features.forEach((feature) => {
                const countryName = mapCountryName(feature.properties.ADMIN);
                const value = feature.properties.value || 0;
                
                if (countries.includes(countryName)) {
                    const centroid = turf.centroid(feature);

                    const markerPopupContent = `
                        <h3 style="color: black;">${countryName}</h3>
                        <p style="color: black;">No. of Active Issues: ${value.toFixed(2)}</p>
                    `;
                    const markerPopup = new mapboxgl.Popup({ offset: 25 }).setHTML(markerPopupContent);

                    const marker = new mapboxgl.Marker({ color: 'blue' })
                        .setLngLat(centroid.geometry.coordinates)
                        .addTo(map.current);

                    marker.getElement().addEventListener('mouseenter', () => {
                        markerPopup.setLngLat(centroid.geometry.coordinates).addTo(map.current);
                    });

                    marker.getElement().addEventListener('mouseleave', () => {
                        markerPopup.remove();
                    });

                    marker.getElement().addEventListener('click', () => {
                        window.location.href = `http://localhost:3001/countries/${encodeURIComponent(countryName)}`;
                    });
                }
            });
        });
    }, [countryBoundaries]);

    return (
        <div className="h-full w-full bg-[#000230] relative flex flex-col">
            <h1 className="text-3xl font-bold text-white bg-opacity-20 bg-blue px-4 py-2 rounded-md shadow-lg text-center">
                Global Overview
            </h1>
            <div
                ref={mapContainer}
                className="flex-grow rounded-lg shadow-lg border border-gray-600 overflow-hidden mt-2"
            />
        </div>
    );
};

export default GlobalOverview;