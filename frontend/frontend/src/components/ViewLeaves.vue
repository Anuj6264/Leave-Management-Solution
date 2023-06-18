<template>
  <div>
    <h2>VIEW LEAVES</h2>
    <div v-if="noLeavesFound">No leaves found</div>
    <table v-else class="leaves-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>From</th>
          <th>To</th>
          <th>Duration (in days)</th>
          <th>Status</th>
          <th>Reason</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="leave in leaves" :key="leave.id">
          <td>{{ leave.firstName }} {{ leave.lastName }}</td>
          <td>{{ formatDate(leave.from_date) }}</td>
          <td>{{ formatDate(leave.to_date) }}</td>
          <td>{{ leave.leave_count }} days</td>
          <td>{{ leave.status }}</td>
          <td>{{ leave.reason }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: 'ViewLeaves',
  data() {
    return {
      leaves: [],
      noLeavesFound: false,
    };
  },
  created() {
    this.fetchLeaves();
  },
  methods: {
    fetchLeaves() {
      this.$http.get('http://127.0.0.1:5000//api/leaves',  
      {
        headers: {
        Authorization: `Bearer ${localStorage.access_token}`}, 
      })
        .then(response => {
          this.leaves = response.data;
          if (this.leaves.length === 0) {
            this.noLeavesFound = true;
          } else {
            this.noLeavesFound = false;
          } 
        })
        .catch(error => {
          console.error(error);
        });
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    },
  },
};
</script>

<style>
h2 {
 font-size: 40px;
 color:red;
}
.leaves-table {
  width: 100%;
  border-collapse: collapse;
}

.leaves-table th,
.leaves-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.leaves-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.leaves-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.leaves-table tbody tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}
</style>
