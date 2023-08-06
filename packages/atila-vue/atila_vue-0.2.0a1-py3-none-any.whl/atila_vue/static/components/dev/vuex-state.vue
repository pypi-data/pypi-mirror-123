<template>
  <article v-if='$debug' class='container'>
    <div class='article'>
      <h5>Vuex State</h5>
      <ul id='vuex-state'>
        <div v-for='[k, v] in Object.entries($store.state)'>
          <li class='mb-0' v-if="k != 'context'">{{ k }}: {{ v }}</li>
        </div>
        <li>context
          <ul>
            <li class='mb-0' v-for='[k, v] of Object.entries(contextOrEmpty)'>
              {{ k }}: {{ v }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div v-if='hasRouter' class='router'>
      <h5>Vue Router</h5>
      <ul>
        <li class='mb-0'>$route: {name: "{{$route.name}}", path: "{{$route.path}}", query: {{$route.query}} } </li>
        <li class='mb-0'>$router.options.base: "{{ $router.options.base }}" </li>
        <li class='mb-0'>$router.options.routes
          <ul>
            <li v-for='r of $router.options.routes'>{{ r }}</li>
          </ul>
        </li>
      </ul>
    </div>
  </article>
</template>

<style scoped>
  .article {
    color: #4904b3;
    word-break: break-all;
    margin-right: 32px;
  }
  .router {
    color: #138535;
    word-break: break-all;
    margin-right: 32px;
  }
</style>

<script>
  export default {
    computed: {
      ...mapVuexItems (),
      contextOrEmpty () {
        return this.context || {}
      },
      hasRouter () {
        return !!router
      }
    },
  }
</script>
