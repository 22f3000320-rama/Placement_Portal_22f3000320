<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-7 mt-4">
                <h2 class="mb-3">Students that match your filters:</h2>
                <div v-if="isLoading" class="text-center my-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2 text-muted">Fetching students...</p>
                </div>
                <div v-else-if="studentsList.length === 0" class="alert alert-warning shadow-sm" role="alert">
                    No students found matching your criteria.
                </div>
                <div v-else class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">Sr no.</th>
                                <th scope="col">Name</th>
                                <th scope="col">Department</th>
                                <th scope="col">CGPA</th>
                                <th scope="col">Graduation Year</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(student,index) in studentsList" :key="student.student_id">
                                <td>{{ index+1 }}</td>
                                <td>{{ student.name }}</td>
                                <td>{{ student.department }}</td>
                                <td>{{ student.cgpa }}</td>
                                <td>{{ student.year }}</td>
                                <td><button class="btn btn-outline-primary btn-sm"
                                        @click="viewStudent(student.student_id)">View Details</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="text-center mt-4">
                    <button class="btn btn-outline-success" @click="this.$router.back()">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'AdminSearchStudents',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                isLoading: true,
                studentsList: []
            }
        },
        methods: {
            async fetchFilteredStudents(filters) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-searched-students', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        },
                        params: filters
                    });
                    this.studentsList = res.data.students
                    console.log(res.data.students)
                } catch (error) {
                    console.error("Failed to fetch filtered students");
                    this.studentsList = [];
                } finally {
                    this.isLoading = false;
                }
            },
            viewStudent(studentId) {
                this.$router.push({
                    name: "admin-student-details",
                    params: {
                        studentId: studentId
                    }
                });
            }
        },
        async mounted() {
            const queryParams = this.$route.query;
            this.fetchFilteredStudents(queryParams);
        }
    }
</script>