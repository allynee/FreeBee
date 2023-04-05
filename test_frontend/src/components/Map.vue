<template>
<div>
    <v-container>
    <gmap-map :center="center" :zoom="12" style="width: 100%; height: 500px">
      <GmapCluster>
        <gmap-info-window :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false">
            <v-icon>mdi-paw</v-icon>
        </gmap-info-window>

        <gmap-marker :key="i" v-for="(m,i) in markers" :position="m.position" :clickable="true" @click="toggleInfoWindow(m,i);">
        </gmap-marker>
      </GmapCluster>
    </gmap-map>
<!--  @click="center=m.position" -->
    </v-container>
</div>

</template> 

<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/markerclustererplus/2.1.4/markerclusterer.js"></script> -->
<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyCsbcA8EHPhaZbxQ_Gubm_ZhQyy-pcn6JM&libraries=places"></script>

<script>
import GmapCluster from 'vue2-google-maps/dist/components/cluster';

export default{
components:{GmapCluster},
props: {
    allPets: Array,
},
data(){
    return{
        center: {
            lat: 1.3521,
            lng: 103.8198
        },
        click: false,
        // info window nonsense
        infoWindowPos: null,
        infoWinOpen: false,
        currentMidx: null,
        infoOptions: { 
            content: "",
            //help info window sit above our marker
            pixelOffset: {
                width: 0,
                height: -45
            }
        },

}
},
methods: {
    toggleInfoWindow: function(marker, idx) {
        this.infoWindowPos = marker.position;
        // marker.infoText += ` <span style="width:100%; text-align: center">
        //             <button type="button" onclick="${this.redirect(pet.petid)}">Click Me</button>
        //          </span>`
        this.infoOptions.content = marker.infoText;
        this.center = marker.position;

        //check if its the same marker that was selected if yes toggle
        if (this.currentMidx == idx) {
              this.infoWinOpen = !this.infoWinOpen;
        }
        
        //if different marker set infowindow to open and reset current marker index
        else {
            this.infoWinOpen = true;
            this.currentMidx = idx;
        }
    },
    test(){
        console.log("test");
    }
},
computed: {
    markers(){
        // console.log(this.allPets)
        let markers = [];
        let lat=1.3691;
        let lng = 103.8454;
        this.allPets.forEach(pet => {

            let petid=pet.petid
            let myLat = pet.petGeoLoc.lat;
            let myLng = pet.petGeoLoc.lng;
            let petObj = {
                position: {
                    lat: myLat,
                    lng: myLng
                },
                infoText: 
                `   
                <div style="display:flex ; flex-wrap: wrap; align-items: center; justify-content: center; 
                width: 225px; height: 400px; background-color: #EFEBE9; padding: 5px 0px 5px 0px">
                <span style="margin:5px; width:100%; text-align: center">${pet.petLocation}</span>
                <h2 style="width:100%;text-align: center; margin: 3px 5px 3px 5px">${pet.petName}</h2>

                <span style="width:150px; margin: 3px 1px 3px 1px; ">
                    <img src="${pet.image}" style="max-height:200px;width:100%;"/>
                </span>
                
                </span>
                <span style="margin:5px; width:100%; text-align: center">Last Seen Date: ${pet.petDate}</span>
                </span>
                <span style="margin:5px; width:100%; text-align: center">Breed: ${pet.petBreed}</span>
                </span>
                <span style="margin:5px; width:100%; text-align: center">Gender: ${pet.petGender}</span>
                
                </div>
                `
                // <span style="margin:5px; width:100%; text-align: center"> ${pet.petLocation}</span>
                // <a href="SearchAllPets/${petid}"><span>Click</span></a>          
                // <span style="background-color:#BCAAA4;padding:5px; margin:5px; width: 120px;"><a href="/SearchAllPets/${pet.petid}">Haiz </a></span>
            };
            markers.push(petObj);
        });
        return markers;
        //                 <button style="background-color:#BCAAA4;padding:5px; margin:5px; width: 120px;"
        //                 onclick="${this.redirect(pet.petid)}"
        // >View More Details</button>
    }
},
} 
</script>
