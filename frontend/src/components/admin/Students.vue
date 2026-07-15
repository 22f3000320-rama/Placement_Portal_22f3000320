<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-8 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Students...</p>
                </div>
                <div v-else-if="!students" class="alert alert-warning shadow-sm" role="alert">
                    Students Not Found.
                </div>
                <div v-else>
                    <header class="d-flex justify-content-between align-items-center mb-4">
                        <h2 class="mb-3">Students</h2>
                        <span v-if="role==='admin'" class="badge bg-success px-3 py-2">{{ studentCount }}</span>
                    </header>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Email</th>
                                    <th scope="col">Department</th>
                                    <th class="d-flex justify-content-center" scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(student,index) in students" :key="student.email">
                                    <td>{{ index+1 }}</td>
                                    <td>{{ student.name }}</td>
                                    <td>{{ student.email }}</td>
                                    <td>{{ student.department }}</td>
                                    <td class="d-flex gap-2 justify-content-end"><button
                                            class="btn btn-outline-primary btn-sm"
                                            @click="viewStudent(student.student_id)">View Details</button>
                                        <button v-if="role==='admin'" class="btn btn-outline-danger btn-sm"
                                            @click="blacklistStudent(student.student_id)">{{ student.is_active ?
                                            'UnBlock':'Block' }}</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'Students',
        props: { role: String },
        data() {
            return {
                students: [],
                studentCount: null,
                isLoading: true,
            }
        },
        methods: {
            async fetchStudents() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/admin/get-students', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    this.studentCount = res.data.studentCount;
                    this.students = res.data.students;
                } catch (error) {
                    console.error('Failed to fetch students.', error);
                    this.students = [];
                } finally {
                    this.isLoading = false;
                }
            },
            viewStudent(studentId) {
                this.$router.push({ name: 'admin-student-details', params: { studentId } })
            }
        },
        async blacklistStudent(studentId) {
            const token = localStorage.getItem('access_token');
            try {
                const res = await axios.post(`http://localhost:5000/api/admin/blacklist-student/${studentId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );
                alert(res.data.message)
                this.fetchStudents();
            }
            catch (error) {
                alert(error.response.data.message);
                console.error('Blacklisting Student Failed: ', error);
            }
        },
        mounted() {
            this.fetchStudents();
        }
    }
</script>