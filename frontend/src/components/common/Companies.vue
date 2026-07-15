<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-9 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Companies...</p>
                </div>
                <div v-else-if="!companies" class="alert alert-warning shadow-sm" role="alert">
                    Companies Not Found.
                </div>
                <div v-else>
                    <header class="d-flex justify-content-between align-items-center mb-4">
                        <h2 class="mb-3">Companies</h2>
                        <span v-if="role==='admin'" class="badge bg-success px-3 py-2">{{ companyCount }}</span>
                    </header>
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
                                <tr v-for="(company,index) in companies" :key="company.email">
                                    <td>{{ index+1 }}</td>
                                    <td>{{ company.name }}</td>
                                    <td>{{ company.email }}</td>
                                    <td>{{ company.website }}</td>
                                    <td class="d-flex gap-2 justify-content-end"><button
                                            class="btn btn-outline-primary btn-sm me-2"
                                            @click="viewCompany(company.company_id)">View Details</button>
                                        <button v-if="role==='admin'" class="btn btn-outline-danger btn-sm"
                                            @click="blackListUnBlacklistCompany(company.company_id)">{{
                                            company.is_active ?
                                            'Block' : 'Unblock' }}</button>
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
        name: 'Companies',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                companies: [],
                companyCount: null,
                isLoading : true,
            }
        },
        methods: {
            async fetchCompanies() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-companies', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    this.companyCount = res.data.companyCount;
                    this.companies = res.data.companies;
                } catch (error) {
                    console.error('Failed to fetch companies.', error);
                    this.companies = [];
                } finally{
                    this.isLoading = false;
                }
            },
            viewCompany(companyId) {
                if (this.role === 'admin') {
                    this.$router.push({
                        name: "admin-company-details",
                        params: {
                            companyId: companyId
                        }
                    });
                } else {
                    this.$router.push({
                        name: "student-company-details",
                        params: {
                            companyId: companyId
                        }
                    });
                }
            },
            async blackListUnBlacklistCompany(companyId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.post(`http://localhost:5000/api/admin/blacklist-unblacklist-company/${companyId}`, {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );

                    this.fetchCompanies();
                } catch (error) {
                    alert(error.response.data.message);
                    alert("Failed to Update Company Blacklisting Status.");
                }
            },
        },
        mounted() {
            console.log(this)
            console.log("here")
            this.fetchCompanies();
        }
    }
</script>