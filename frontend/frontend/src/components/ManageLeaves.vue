<template>
  <div class="manage-leaves">
    <h2>MANAGE LEAVES</h2>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>From</th>
          <th>To</th>
          <th>Duration (in days)</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="leave in leaves" :key="leave.id" class="leave-item">
          <td>{{ leave.firstName }} {{ leave.lastName }}</td>
          <td>{{ formatDate(leave.from_date) }}</td>
          <td>{{ formatDate(leave.to_date) }}</td>
          <td>{{ leave.leave_count }}</td>
          <td>{{ leave.status }}</td>
          <td>
            <div v-if="leave.status === 'pending'" class="action-buttons">
              <button @click="acceptLeave(leave.id)">Accept</button>
              <button class="reject" @click="rejectLeave(leave.id)">Reject</button>
              <input type="text" v-model="leave.reason" placeholder="Reason for rejection" />
            </div>
            <div v-else-if="leave.status === 'accepted'" class="status accepted">
              Accepted
            </div>
            <div v-else-if="leave.status === 'rejected'" class="status rejected">
              Rejected: {{ leave.reason }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: 'ManageLeaves',
  data() {
    return {
      leaves: [],
    };
  },
  created() {
    this.fetchLeaves();
  },
  methods: {
    fetchLeaves() {
      console.log("Entered fetch function")
      this.$http
        .get("http://localhost:5000/api/leaves/all", {
           headers: {
           Authorization: `Bearer ${localStorage.access_token}`},
        })
        .then((response) => {
          console.log(response.data)
          this.leaves = response.data;
        })
        .catch((error) => {
          console.error(error);
        });

    },
    acceptLeave(leaveId) {
      console.log(localStorage.access_token)
      this.$http
        .patch(`http://localhost:5000/api/leaves/${leaveId}`, {status: 'accepted' },{
        headers: {
        Authorization: `Bearer ${localStorage.access_token}`},
      })
        .then(() => {
          this.fetchLeaves();
          alert("Leave Accepted Successfully")
        })
        .catch((error) => {
          console.error(error);
          alert("Some error occured. Please try again")
        });
    },
    rejectLeave(leaveId) {
      const leave = this.leaves.find((leave) => leave.id === leaveId);
      if (leave) {
        if (!leave.reason) {
          alert("Please provide a reason for rejection.");
          return;
        }
        this.$http
          .patch(`http://localhost:5000/api/leaves/${leaveId}`, { reason: leave.reason, status: 'rejected'}, {
        headers: {
        Authorization: `Bearer ${localStorage.access_token}`}, 
      })
          .then(() => {
            this.fetchLeaves();
            alert("Leave Rejected Successfully")
          })
          .catch((error) => {
            console.error(error);
            alert("Some error occured. Please try again")
          });
      }
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
.manage-leaves {
  margin: 20px;
}

.manage-leaves h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  border: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}

.leave-item {
  font-size: 14px;
}

.action-buttons {
  display: flex;
  align-items: center;
}

.action-buttons button {
  margin-right: 5px;
  padding: 8px 12px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-buttons button.reject {
  background-color: #f44336;
}

.action-buttons button.reject:hover {
  background-color: #f44336d7;
}

.action-buttons button:hover {
  background-color: #45a049;
}



.action-buttons input[type="text"] {
  flex: 1;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.status {
  padding: 5px;
  font-weight: bold;
  text-align: center;
}

.accepted {
  background-color: #c6efce;
}

.rejected {
  background-color: #f8d7da;
}
</style>