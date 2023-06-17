<template>
    <header>
      <nav>
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/login">Login</router-link></li>
          <li><router-link to="/register">Register</router-link></li>
          <li><router-link to="/apply-leave">Apply Leave</router-link></li>
          <li><router-link to="/view-leaves">View Leaves</router-link></li>
          <li><router-link to="/manage-leaves">Manage Leaves</router-link></li>
        </ul>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: 'Header',
  };
  </script>
  
  <style scoped>
  header {
    background-color: #333;
    color: #fff;
    padding: 10px;
  }
  
  nav ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: space-around;
  }
  
  nav ul li {
    display: inline-block;
  }
  
  nav ul li a {
    color: #fff;
    text-decoration: none;
    padding: 10px;
  }
  
  nav ul li a:hover {
    background-color: #666;
  }
  </style>
  