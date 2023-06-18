<template>
  <div>
    <h2 class="register-form">REGISTER</h2>
    <form class="register-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <div class="form-group">
        <label for="firstName">First Name:</label>
        <input type="firstName" id="firstName" v-model="firstName" />
      </div>
      <div class="form-group">
        <label for="lastName">Last Name:</label>
        <input type="lastName" id="lastName" v-model="lastName" />
      </div>
      <div class="form-group">
        <label for="role">Role:</label>
        <div>
          <input type="radio" id="employee" value="Employee" v-model="role" />
          <label for="employee">Employee</label>
        </div>
        <div>
          <input type="radio" id="manager" value="Manager" v-model="role" />
          <label for="manager">Manager</label>
        </div>
      </div>

      <button @click.prevent="register">Register</button>
    </form> 
  </div>
  </template>
  
  <script>

  export default {
    name: 'Register',
    data() {
      return {
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        role: ''
      };
    },
    methods: {
      register() {
        this.$http.post('http://127.0.0.1:5000//api/register', 
        { 
          username: this.username,
          password: this.password, 
          firstName: this.firstName, 
          lastName: this.lastName,
          role: this.role,
          })
        .then(response => {
         alert("User Registered Successfully. Redirecting to login")
         this.$router.push('/login')
        })
        .catch(error => {
          alert("Could Not Register. Please try again")
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
}

.register-form {
  display: flex;
  flex-direction: column;
  max-width: 200px;
  margin-left: 660px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="password"],
input[type="firstName"],
input[type="lastName"] {
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

.radio-group {
  margin-bottom: 1rem;
}

.radio-group label {
  display: inline-block;
  margin-right: 1rem;
}

.radio-group input[type="radio"] {
  display: none;
}

.radio-group input[type="radio"] + label:before {
  content: '';
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid #007bff;
  margin-right: 4px;
  vertical-align: middle;
}

.radio-group input[type="radio"]:checked + label:before {
  background-color: #007bff;
}

.radio-group input[type="radio"]:focus + label:before {
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5);
}
</style>