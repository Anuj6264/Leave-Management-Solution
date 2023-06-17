<template>
    <div>
    <h2>LOGIN</h2>
    <form class="login-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <button @click.prevent="login">Login</button>
    </form>
  </div>
  </template>
  
  <script>
  
  export default {
    name: 'Login',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      login() {
        console.log("Entered Login Function")
        this.$http.post('http://localhost:5000/api/login', { username: this.username, password: this.password })
        .then(response => {
          alert("Logged In successfully")
          const access_token = response.data.access_token;
          localStorage.setItem('access_token', access_token);
          const userRole = response.data.user.role; 
          localStorage.setItem('user_role', userRole)
        })
        .catch(error => {
          alert("Could Not Login. Please check the credentials and try again")
          console.log(error.response.data.message);
        });
      },
    },
  };
</script>

<style scoped>
h2 {
  font-size: 40px;
  font-weight: bold;
  margin-top: 40px;
  color: red;
  margin-left: 30px;
}

.login-form {
  margin-top: 50px;
  margin-left: 670px;
  display: flex;
  flex-direction: column;
  max-width: 200px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100px;
  margin-left: 50px;
}

button:hover {
  background-color: #0056b3;
}

button:active {
  background-color: #004080;
}
</style>
  