<template>
  <div class = "apply-leaves">
    <h1>APPLY LEAVES</h1>
    <label for="startDate">Start Date :</label>
    <datepicker v-model="fromDate" format="DD-MM-YYYY"></datepicker>

    <label for="endDate">End Date :</label>
    <datepicker v-model="toDate" format="DD-MM-YYYY"></datepicker>

    <button @click="applyLeave">Submit</button>
  </div>
</template>

<script>
import Datepicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
import moment from 'moment';

export default {
  name: 'ApplyLeave',
  components: {
    Datepicker
  },
  data() {
    return {
      fromDate: null,
      toDate: null,
    };
  },
  methods: { 
    applyLeave() {
      if (!this.fromDate || !this.toDate) {
        alert('Please select both Start and End Date.');
        return;
      }

      const leaveData = {
        from_date: moment(this.fromDate, 'DD-MM-YYYY').format('YYYY-MM-DD'),
        to_date: moment(this.toDate, 'DD-MM-YYYY').format('YYYY-MM-DD'),
      };

      console.log(leaveData.from_date, leaveData.to_date)

      this.$http
        .post('http://127.0.0.1:5000//api/leaves', leaveData, {
        headers: {
        Authorization: `Bearer ${localStorage.access_token}`}, 
      })
        .then(response => {
          alert('Leaves applied successfully.');
      })
        .catch(error => {
          console.error(error);
          alert("Leaves can't be processed. Please check if the selected date range is less than 15 days and End date exceeds Start date.");
      });
    },
  }
};
</script>

<style scoped>
.apply-leaves {
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  text-align: center;
  color: red;
  margin-top: 50px;
  font-size: 40px;
}

label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
  color: #555;
}

button {
  display: block;
  margin-top: 20px;
  padding: 10px 50px;
  align-items: center;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.datepicker-wrapper {
  display: inline-block;
  margin-top: 5px;
}

.datepicker input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.datepicker-calendar-container {
  position: absolute;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 9999;
  padding: 10px;
  margin-top: 5px;
}

.datepicker-calendar {
  width: 220px;
  max-height: 250px;
  overflow-y: auto;
}

.datepicker-calendar table {
  width: 100%;
}

.datepicker-calendar th,
.datepicker-calendar td {
  text-align: center;
  padding: 5px;
}

.datepicker-calendar .prev-month,
.datepicker-calendar .next-month {
  color: #ccc;
  cursor: pointer;
}

.datepicker-calendar .selected {
  background-color: #007bff;
  color: #fff;
}

.datepicker-calendar .today {
  background-color: #f2f2f2;
}

.datepicker-calendar .disabled {
  color: #ccc;
  cursor: not-allowed;
}

</style>
