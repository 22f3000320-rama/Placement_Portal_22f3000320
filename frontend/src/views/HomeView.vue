<template>
  <main>
    <div>
      <h1>Welcome to the Placement Portal</h1>
      <p>This is the home page. Use the buttons below to explore the portal.</p>
    </div>
    <div>
      <div @click="$router.push('/admin')">
        Admin Dashboard
      </div>
    </div>
    <div>
      <div @click="$router.push('/student')">
        Student Dashboard
      </div>
    </div>
    <div>
      <div @click="$router.push('/company')">
        Company Dashboard
      </div>
    </div>
  </main>
</template>

<script>
  export default {
    name: 'HomeView'
  }
</script>