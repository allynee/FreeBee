<template>
  <div>
    <v-btn @click="uploadImage">Upload</v-btn>
    <input
      type="file"
      style="display: none"
      ref="fileInput"
      accept="image/*"
      @change="onFilePicked"
    />

    <img v-if="imageUrl != ''" :src="imageUrl" height="150" class="date" />
    <v-btn @click="onSubmit">Submit</v-btn>
    <img v-if="imagePost" :src="imagePost" />
  </div>
</template>

<script>
const axios = require("axios");

export default {
  data() {
    return { imageUrl: null, image: null, imagePost: null };
  },
  methods: {
    uploadImage() {
      this.$refs.fileInput.click();
    },
    // running the input function, pushing a preview of the image file
    onFilePicked(event) {
      console.log(event.target);
      const file = event.target.files;

      let filename = file[0].name;
      if (filename.lastIndexOf(".") <= 0) {
        return alert("Not a valid file");
      }
      const fileReader = new FileReader();
      fileReader.onload = () => {
        this.imageUrl = fileReader.result;
      };
      fileReader.readAsDataURL(file[0]);
      this.image = file[0];
    },
    async onSubmit() {
      const formData = new FormData();
      formData.append("image", this.image, this.image.name);
      // let ext = filename.slice(filename.lastIndexOf('.'));
      axios.post(`http://localhost:3002/image`, formData).then((response) => {
        let listingid = response.data.listingid;
        let ext = response.data.extension;
        this.imagePost = `https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F${
          listingid + ext
        }?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4`;
        console.log(this.imagePost);
      });
    },
  },
};
</script>
