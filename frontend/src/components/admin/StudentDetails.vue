<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="card shadow-sm rounded-3">
                    <div v-if="isLoading" class="text-center my-5">
                        <p class="mt-2 text-muted">Fetching Student Details...</p>
                    </div>
                    <div v-else-if="!student" class="alert alert-warning shadow-sm" role="alert">
                        Student NOT Found.
                    </div>
                    <div v-else class="card-body p-4">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h4 class="card-title mb-1">
                                    {{ student.name }}
                                </h4>

                                <p class="text-muted mb-3">
                                    {{ student.email }}
                                </p>
                            </div>
                            <div class="rounded-circle bg-primary text-white
                    d-flex justify-content-center align-items-center" style="width: 60px; height: 60px;">
                                {{ student.name.charAt(0).toUpperCase() }}
                            </div>

                        </div>
                        <div class="mt-3">

                            <p class="card-text">
                                <strong>Department:</strong> {{ student.department }}
                            </p>
                            <p class="card-text">
                                <strong>CGPA:</strong> {{ student.cgpa }}
                            </p>
                            <p class="card-text">
                                <strong>Graduation Year:</strong> {{ student.year }}
                            </p>
                            <p class="card-text">
                                <strong>Contact:</strong> {{ student.contact }}
                            </p>
                            <p class="card-text">
                                <strong>Skills:</strong> {{ student.skills.join(', ') }}
                            </p>
                        </div>
                        <div class=" text-center mt-4"><button class="btn btn-outline-primary me-2"
                                @click="this.$router.push({name: 'admin-student-application-history' , params: { studentId: student.student_id }} )">View
                                Application History</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="text-center mt-4">
        <button class="btn btn-outline-success" @click="this.$router.back()">Close</button>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'StudentDetails',
        data() {
            return {
                student: null,
                isLoading:true,
            }
        },
        methods: {
            async fetchStudentDetails() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get(
                        `http://localhost:5000/api/get-student-details/${this.$route.params.studentId}`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    this.student = res.data.student;
                }
                catch (error) {
                    console.error('Failed to fetch student:', error);
                    alert(error.response.data.message);
                } finally {
                    this.isLoading=false;
                }
            }
        },
        mounted() {
            this.fetchStudentDetails();
        }
    }
</script>