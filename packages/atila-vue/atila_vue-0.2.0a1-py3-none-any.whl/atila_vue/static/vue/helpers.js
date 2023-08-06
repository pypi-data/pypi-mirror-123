// define prototype methods -----------------------------------
Number.prototype.format = function () {
  if(this==0) return "0"
  var reg = /(^[+-]?\d+)(\d{3})/
  var n = (this + '')
  while (reg.test(n)) n = n.replace (reg, '$1' + ',' + '$2')
    return n
}
String.prototype.format = function () {
  var num = parseFloat (this)
  if( isNaN(num) ) return "0"
  return num.format ()
}
String.prototype.titleCase = function () {
  return this.replace (/\w\S*/g, function (txt) {return txt.charAt(0).toUpperCase () + txt.substr (1).toLowerCase ();})
}
Date.prototype.format = function(f) {
  if (!this.valueOf()) return " "
  var d = this;
  return f.replace(/(%Y|%y|%m|%d|%H|%I|%M|%S|%p|%a|%A|%b|%B|%w|%c|%x|%X|%k|%n|%D)/gi, function($1) {
    switch ($1) {
    case "%Y":
      return d.getFullYear()
    case "%y":
      return (d.getFullYear() % 1000).zfill(2)
    case "%m":
      return (d.getMonth() + 1).zfill(2)
    case "%d":
      return d.getDate().zfill(2);
    case "%H":
      return d.getHours().zfill(2)
    case "%I":
      return ((h = d.getHours() % 12) ? h : 12).zfill(2)
    case "%M":
      return d.getMinutes().zfill(2)
    case "%S":
      return d.getSeconds().zfill(2)
    case "%p":
      return d.getHours() < 12 ? "AM" : "PM"
    case "%w":
      return d.getDay()
    case "%c":
      return d.toLocaleString()
    case "%x":
      return d.toLocaleDateString()
    case "%X":
      return d.toLocaleTimeString()
    case "%b":
      return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()]
    case "%B":
      return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()]
    case "%a":
      return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][d.getDay()]
    case "%A":
      return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()]
    case "%k":
      return ['일', '월', '화', '수', '목', '금', '토'][d.getDay()]
    case "%n":
      return ( d.getMonth() + 1)
    case "%D":
      return d.getDate()
    default:
      return $1
    }
  })
}
String.prototype.repeat = function(len){var s = '', i = 0; while (i++ < len) { s += this; } return s;}
String.prototype.zfill = function(len){return "0".repeat(len - this.length) + this}
Number.prototype.zfill = function(len){return this.toString().zfill(len)}


// utilities ---------------------------------------------
function load_script (src, callback = () => {}) {
  let current = null
  if (typeof (src) === "string") {
    current = src
    src = []
  } else {
    current = src.shift ()
  }
  var script = document.createElement('script')
  script.setAttribute('src', current)
  script.setAttribute('async', true)
  if (src.length) {
    script.addEventListener('load', () => { this.$load_script (src, callback) })
  } else {
    script.addEventListener('load', callback)
  }
  document.head.appendChild(script)
}

function notify (title, message, icon, timeout = 5000) {
  var options = {
    body: message,
    icon: icon
  }
  const n = new Notification(title, options)
  n.onclick = (event) => {
  n.close ()
  }
  n.onshow = (event) => {
  setTimeout(function(){ n.close () }, timeout)
  }
}

function log (msg, type = 'info') {
  if (Vuex.useStore ().state.$debug) {
    console.log (`[${type}] ${msg}`)
  }
}

function set_cloak (flag) {
  Vuex.useStore ().state.$cloak = flag
}

function traceback (e) {
  let msg = ''
  if (e.response !== undefined) {
    const r = e.response
    let code = r.data.code || 70000
    let message = r.data.message || 'no message'
    log (JSON.stringify(r.data), 'expt')
    msg = `${message} (status: ${r.status}, error: ${code})`
  }
  else {
    msg = `${e.name}: ${e.message}`
  }
  console.log (e)
  log (e, 'expt')
  return msg
}

function sleep (ms) {
  return new Promise (resolve => setTimeout(resolve, ms))
}

function urlfor (name, args = [], _kargs = {}) {
  const urlspecs = Vuex.useStore ().state.$urlspecs
  const target = urlspecs [name]
  if (!target) {
    throw new Error (`route ${name} not found`)
  }

  let url = target.path

  let kargs = {}
  if (Object.prototype.toString.call(args).indexOf ("Array") != -1) {
    let i = 0
    for (let k of target.params) {
      kargs [k] = args [i]
      i += 1
    }
    for (let k of target.query) {
      kargs [k] = args [i]
      i += 1
    }
  } else {
   kargs = args
  }

  for (let k of target.params) {
    if (kargs [k] !== undefined ) {
      url = url.replace (":" + k, kargs [k])
    }
  }

  let newquery = ''
  for (let k of target.query) {
    if (kargs [k] === undefined ) {
      continue
    }
  const v = kargs [k]
  if (!!newquery) {
    newquery += '&'
  }
  newquery += k + "=" + encodeURIComponent (v)
  }

  if (!!newquery) {
    return url + "?" + newquery
  }
  return url
}

function build_url (baseurl, kargs = {}) {
  let url = baseurl
  let newquery = ''
  for (let [k, v] of Object.entries (kargs)) {
    if (v === null) {
      continue
    }
  if (!!newquery) {
    newquery += '&'
  }
  newquery += k + "=" + encodeURIComponent (v)
  }
  if (!!newquery) {
    return url + "?" + newquery
  }
  return url
}

const _deviceDetect = {
  android: function() {
    return navigator.userAgent.match(/Android/i)
  },
  ios: function() {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i)
  },
  mobile: function() {
    return (deviceDetect.android() || deviceDetect.ios())
  },
  touchable: function () {
    return (navigator.maxTouchPoints || 'ontouchstart' in document.documentElement)
  },
  rotatable: function () {
    return window.orientation > -1
  },
  width: function () {
    return window.innerWidth
  },
  height: function () {
    return window.innerHeight
  }
}

function date (dt = null) {
  if (dt === null) {
    return new Date ()
  }
  if (dt.indexOf ('-') === -1) {
    return new Date (parseFloat (dt) * 1000.)
  }
  const [a, b] = dt.split (' ')
  const [Y, m, d] = a.split ("-")
  const [H, M, S] = b.substring (0, 8).split (":")
  return new Date (Date.UTC (Y, parseInt (m) - 1, d, H, M, S))
}

function _check_url (url) {
  if (url.substring (0, 1) == '/') {
    throw new Error ('url cannot be started with /')
  }
}

function staticfor (url) {
  _check_url (url)
  return Vuex.useStore ().state.$static_url + url
}

function mediafor (url) {
  _check_url (url)
  return Vuex.useStore ().state.$media_url + url
}

exports.log = log
exports.traceback = traceback
exports.urlfor = urlfor
exports.mediafor = mediafor
exports.staticfor = staticfor
exports.set_cloak = set_cloak
exports.load_script = load_script
exports.notify = notify
exports.sleep = sleep
exports.build_url = build_url
exports.device = _deviceDetect
exports.date = date


// websocket ---------------------------------------------------
class AsynWebSocket {
  constructor (url, read_handler) {
    this.url = url
    this.read_handler = read_handler
    this.sock = null
    this.buffer = []
    this.connected = false
    this.connect (url, read_handler)
  }

  connectex () {
    this.sock = new WebSocket (this.url)
    this.sock.onopen = this.handle_connect
    this.sock.onclose = this.handle_close
    this.sock.onerror = this.handle_error
    this.sock.onmessage = this.read_handler
  }

  handle_connect() {
    this.connected = true
    log ('connected', 'websocket')
    this.handle_write ()
  }

  handle_write () {
    for (var i = 0; i < this.buffer.length; i++) {
      msg = this.buffer.shift ()
      log (`send: ${ msg }`, 'websocket')
      this.sock.send (msg)
    }
  }

  handle_close (evt) {
    this.sock = null
    log ('closed', 'websocket')
  }

  handle_error (evt)	{
    log (evt.data, 'error')
  }

  connect (url, read_handler = (evt) => log (evt.data)) {
    // lazy connect on wpush, it is more reliable on disconnected
    if (url.indexOf ('/') == 0) {
      url = location.origin.replace(/^http/, 'ws') + url
    }
  }

  close (evt) {
    this.connected = false
    this.sock.close ()
  }

  push (msg) {
    if (!msg) { return }

    this.buffer.push (msg)
    if (this.sock == null) {
        this.connectex ()
        return
    }
    if (!this.connected) {
      return
    }
    this.handle_write ()
  }
}

function create_websocket (url, read_handler) {
  const ws = new AsynWebSocket (url, read_handler)
  Vuex.useStore ().state.$websocket = ws
  return ws
}

exports.create_websocket = create_websocket


// vue & vuex Shorcuts ----------------------------------------
exports.$http = axios
exports.ref = Vue.ref;
exports.computed = Vue.computed
exports.watch = Vue.watch
exports.watchEffect = Vue.watchEffect
exports.getCurrentInstance = Vue.getCurrentInstance
exports.inject = Vue.inject
exports.provide = Vue.provide
exports.InjectionKey = Vue.InjectionKey
exports.onBeforeMount = Vue.onBeforeMount
exports.onMounted = Vue.onMounted
exports.onBeforeUpdate = Vue.onBeforeUpdate
exports.onUpdated = Vue.onUpdated
exports.onBeforeUnmount = Vue.onBeforeUnmount
exports.onUnmounted = Vue.onUnmounted
exports.onErrorCaptured = Vue.onErrorCaptured
exports.onRenderTracked = Vue.onRenderTracked
exports.onRenderTriggered = Vue.onRenderTriggered

exports.useStore = Vuex.useStore
exports.mapState = Vuex.mapState
exports.mapGetters = Vuex.mapGetters
exports.mapActions = Vuex.mapActions
exports.mapMutations = Vuex.mapMutations

exports.useRouter = VueRouter.useRouter
exports.useRoute = VueRouter.useRoute


// vuex mappers for coposition API -----------------------------
// https://gist.github.com/ub3rb3457/586467f2cbd54d0c96d60e16b247d151
// ex) const { countUp, countDown } = useState ()
const useState = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store.state).map(key => [key, Vue.computed(() => store.state[key])]))
}

const useGetters = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store.getters).map(getter => [getter, Vue.computed(() => store.getters[getter])]))
}

const useMutations = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store._mutations).map(mutation => [mutation, value => store.commit(mutation, value)]))
}

const useActions = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store._actions).map(action => [action, value => store.dispatch(action, value)]))
}

exports.useState = useState
exports.useGetters = useGetters
exports.useMutations = useMutations
exports.useActions = useActions
