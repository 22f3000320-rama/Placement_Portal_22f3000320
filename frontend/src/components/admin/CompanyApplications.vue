<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-9 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Company Applications...</p>
                </div>
                <div v-else-if="companyApplications.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No pending Company Application.
                </div>
                <div v-else>
                    <h2 class="mb-3">Company Applications</h2>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Email</th>
                                    <th scope="col">Website</th>
                                    <th class="d-flex justify-content-center" scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(company,index) in companyApplications" :key="company.email">
                                    <td>{{ index+1 }}</td>
                                    <td>{{ company.name }}</td>
                                    <td>{{ company.email }}</td>
                                    <td>{{ company.website }}</td>
                                    <td class="d-flex justify-content-end"><button
                                            class="btn btn-outline-primary btn-sm me-2"
                                            @click="viewCompany(company.company_id)">View Details</button>
                                        <button class="btn btn-outline-success btn-sm me-2"
                                            @click="approveCompany(company.company_id)">Approve</button>
                                        <button class="btn btn-outline-danger btn-sm"
                                            @click="rejectCompany(company.company_id)">Reject</button>
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
        name: 'CompanyApplications',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                companyApplications: [],
                isLoading: true,
            }
        },
        methods: {
            async fetchCompanyApplications() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/admin/get-company-applications', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    console.log(res.data)
                    this.companyApplications = res.data.companyApplications;
                } catch (error) {
                    console.error('Failed to fetch company applications.', error);
                    this.companyApplications = [];
                } finally {
                    this.isLoading = false;
                }
            },
            viewCompany(companyId) {
                this.$router.push({
                    name: 'admin-company-details', params: { companyId }
                })
            },
            async approveCompany(companyId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.patch(`http://localhost:5000/api/admin/approve-company/${companyId}`, {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.fetchCompanyApplications();
                } catch (error) {
                    console.error('Failed Company Approval:', error);
                    alert(error.response.data.message);
                }
            },
            async rejectCompany(companyId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.patch(`http://localhost:5000/api/admin/reject-company/${companyId}`, {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.fetchCompanyApplications();
                } catch (error) {
                    console.error('Failed Company Rejection');
                    alert(error.response.data.message);
                }
            }
        },
        mounted() {
            this.fetchCompanyApplications();
        }
    }
</script>