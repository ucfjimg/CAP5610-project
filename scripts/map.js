let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 39, lng: -98 },
    zoom: 5.5,
  });

   let image = {
      url: 'red-cross-icon.png',
      size: new google.maps.Size(16, 16),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(8, 8)
   };

   let states = ['CA', 'IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']
   for (st in states) {
      let geom = stategeom[states[st]]
      for (pg in geom) {
         let poly = new google.maps.Polygon({
            paths: geom[pg].map(pt => ({lng: pt[0], lat: pt[1]})),
            strokeColor: "#000000",
            fillColor: "#004080",
            strokeWeight: 2,
            strokeOpacity: 0.8,
            fillOpacity: 0.3,
            map
         })
      }
   }

   let stset = new Set(states)
   for (let i in wxstations) {
      let marker = wxstations[i]
      if (!stset.has(marker.state)) {
         continue
      }
      let position = { lat: marker.lat, lng: marker.long };
      new google.maps.Marker({
         position, map, title: marker.name, icon: image
      });
   }
}
