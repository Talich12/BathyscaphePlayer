<template>
  <link
    href="https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap"
    rel="stylesheet"
  />
  <link
    rel="stylesheet"
    href="https://unpkg.com/boxicons@latest/css/boxicons.min.css"
  />

  <div class="fullscreen-player">
    <div :id="elementId" />
  </div>

  <div v-if="isBroken">
    <img :id="no_signal" class="fullscreen-image" v-bind:style="{height: this.height + 'px' }"  src="../source/img/no_signal.png" alt="" >
  </div>

  <div v-if="!isChoosen">
    <img :id="no_signal" class="fullscreen-image" v-bind:style="{height: this.height + 'px' }"  src="../source/img/video.jpg" alt="" >
  </div>

  <div class="loader-container" v-if="isLoading">
    <div class="loader"></div>
    <p class="loading-text"><i class="bx bx-hourglass hourglass-tilt"></i></p>
  </div>

  <div class="sidebar-container" v-bind:style="{top: this.height + 'px' }">
    <div class="sidebar-wrapper">
      <aside :class="['sidebar', { open: showSidebar, closed: !showSidebar }]">
        <div class="sidebar-background">
          <div class="sidebar-header">
            <p style="font-weight: bolder">
              <i class="bx bx-current-location"></i> Bathyscaphe
            </p>
          </div>
          <hr class="rounded" />
          <div class="select-container">
            <div>
              <p class="select-header">
                Currently:
              </p>
              {{ selected }}
            </div>
            <select
              class="custom-select"
              v-model="selectedDevice"
              @change="updateFilteredStreams"
            >
              <option id="mySelect" disabled value="">Select the drone</option>
              <option v-for="device in devices" :key="device">
                {{ device }}
              </option>
            </select>
          </div>
          <hr class="rounded" />
          <div class="fullscreen-container">
            <button
            :class="{ 'disabled-button': isBroken }"
            @click="openFullscreen()" 
            class="sidebar-button">FullScreen<i class='bx bx-fullscreen'></i>
          </button>
          </div>
          <hr class="rounded" />
          <div class="button-list-container">
            <ul>
              <li v-for="(stream, name) in filteredStreams" :key="name">
                <button
                  class="sidebar-button"
                  :name="name"
                  :value="stream.url"
                  @click="handleStreamSelected(name)"
                >
                  <sidebar-item :name="name" :uuid="name"></sidebar-item>
                </button>
              </li>
            </ul>
          </div>
          <hr class="rounded" />
        </div>
      </aside>
      <toggle-button
        v-show="!this.$props.loading"
        :show-sidebar="showSidebar"
        @toggle-sidebar="toggleSidebar"
      ></toggle-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import RTSPtoWEBPlayer from "rtsptowebplayer";
import ToggleButton from "./ToggleButton.vue";
import SidebarItem from "./SidebarItem.vue";
import configData from "../../config.json";

export default {
  name: "PlayerVue",

  computed: {
    filteredStreams() {
      return Object.entries(this.streams).reduce((filtered, [name, stream]) => {
        if (stream.deviceNumber.toString() === this.selectedDevice) {
          const streamStatus = this.checkStreamStatus(stream.url);
          const isBroken = this.brokenStreams.some(
            (brokenStream) => brokenStream.uuid === name
          );
          filtered[name] = { url: stream.url, status: streamStatus, isBroken };
        }
        return filtered;
      }, {});
    },
  },

  props:['loading'],

  data() {
    return {
      serverIP: '',
      isConnected: false,
      isBroken: false,
      isChoosen: false,
      isOnline: navigator.onLine,
      isLoading: false,
      config: {},
      streams: {},
      showSidebar: true,
      devices: [],
      selectedDevice: "",
      elementId: "player",
      brokenStreams: [],
      workingStreams: [],
      height: 0
    };
  },

  methods: {
    initPlayer() {

      if (this.workingStreams.length > 0) {
        const server = this.serverIP + ":8083";
        const uuid = this.workingStreams[0].uuid;
        const channel = "0";
        const source = `http://${server}/stream/${uuid}/channel/${channel}/webrtc?uuid=${uuid}/&channel=${channel}`;

        const options = {
          controls: false,
          parentElement: document.getElementById(this.elementId),
          autoplay: true,
        };
        this.player = new RTSPtoWEBPlayer(options);
        this.player.load(source);
        this.isConnected = true
      }
    },

    async fetchStreams() {
      const serverUrl = "http://" + this.serverIP + ":8083/streams";
      try {
        const response = await axios.get(serverUrl, {
          auth: {
            username: "demo",
            password: "demo",
          },
        });
        const streamsData = response.data.payload;

        this.brokenStreams = [];
        this.workingStreams = [];

        Object.entries(streamsData).forEach(([uuid, streamInfo]) => {
          Object.entries(streamInfo.channels).forEach(
            ([channel, channelInfo]) => {
              const streamObject = {
                uuid,
                channel,
                url: channelInfo.url,
              };

              if (!channelInfo.status || channelInfo.status !== 1) {
                this.brokenStreams.push(streamObject);
              } else {
                this.workingStreams.push(streamObject);
              }
            }
          );
        });
        console.log("Broken Streams:", this.brokenStreams);
        console.log("Working Streams:", this.workingStreams);
      } catch (error) {
        console.error("Error fetching streams:", error);
      }
      if (!this.isConnected){
        this.initPlayer()
      }
    },

    async checkStreamStatus(url) {
      try {
        const response = await fetch(url);
        return response.ok;
      } catch (error) {
        return false;
      }
    },

    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },

    openFullscreen() {
      if (this.isBroken || !this.isOnline){
        return
      }
      var player = document.getElementById(this.elementId)
      if (player.requestFullscreen) {
        player.requestFullscreen();
      } else if (player.mozRequestFullScreen) { /* Firefox */
        player.mozRequestFullScreen();
      } else if (player.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        player.webkitRequestFullscreen();
      } else if (player.msRequestFullscreen) { /* IE/Edge */
        player.msRequestFullscreen();
      }
    },

    handleStreamSelected(uuid) {
      this.isOnline = navigator.onLine
      this.isChoosen = true
      if (this.filteredStreams[uuid].isBroken || !this.isOnline){
        this.isBroken = true
      }
      else{
        this.isBroken = false
      }
      this.isLoading = true;
      this.uuid = uuid;
      const server = this.serverIP + ":8083";
      const channel = "0";
      const source = `http://${server}/stream/${uuid}/channel/${channel}/webrtc?uuid=${uuid}/&channel=${channel}`;

      if (this.isConnected){
        this.player.destroy();
      }
      if (this.isOnline && this.workingStreams.length > 0){
        const options = {
          controls: false,
          parentElement: document.getElementById(this.elementId),
          autoplay: true,
        };
        this.player = new RTSPtoWEBPlayer(options);
        this.player.load(source);
      }
      setTimeout(() => {
          this.isLoading = false;
        }, 1500);
    }
  },

  watch:{
    loading: function() {
      console.log(this.isChoosen)
      const element = document.getElementById(this.elementId);
      let self = this;

      const resizeObserver = new ResizeObserver(function() {
        self.height = element.scrollHeight;
        console.log(self.height)
      });

      resizeObserver.observe(element);
    }
  },

  created() {
    this.initPlayer();
    this.config = configData;
    this.serverIP = this.config.server.serverIP
    console.log(this.serverIP)
    this.streams = Object.entries(this.config.streams).reduce(
      (acc, [uuid, streamData]) => {
        if (streamData.channels && typeof streamData.channels === "object") {
          Object.values(streamData.channels).forEach((channel) => {
            acc[uuid] = {
              deviceNumber: channel.deviceNumber,
              url: channel.url,
            };
          });
        }
        return acc;
      },
      {}
    );

    this.devices = [
      ...new Set(
        Object.values(this.streams).map((stream) => stream.deviceNumber)
      ),
    ];
    this.selectedDevice = this.devices[0].toString();

    this.fetchStreams();
    setInterval(() => {
      this.fetchStreams();
    }, 10000);
  },

  components: {
    SidebarItem,
    ToggleButton,
  },
};
</script>

<style>
@import url("../assets/sidebar.css");


.fullscreen-player {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  position: absolute;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: rgba(0, 0, 0, 0.6);
}

.loader {
  border: 0.4vw solid #23222d;
  border-top: 0.4vw solid #e3e3e3;
  border-bottom: 0.4vw solid #e3e3e3;
  border-radius: 50%;
  width: 7vw;
  height: 7vw;
  animation: spin 4s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  position: absolute;
  font-size: 2.5vw;
  color: #fff;
  text-align: center;
}

.hourglass-tilt {
  animation: tilt 2.5s ease-in-out infinite;
}

@keyframes tilt {
  0%,
  100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
}

.disabled-button {
  opacity: 0.5;
}

.button-list-container {
  height: auto;
  background: linear-gradient(to bottom, #11101d, #11101d);
}
</style>
