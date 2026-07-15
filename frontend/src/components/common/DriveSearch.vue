<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-9 mt-4">
                <h2 class="mb-3">Placement Drives that match your filters:</h2>
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching drives...</p>
                </div>
                <div v-else-if="drivesList.length === 0" class="alert alert-warning shadow-sm" role="alert">
                    No drives found matching your criteria.
                </div>
                <div v-else class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">Sr no.</th>
                                <th scope="col">Drive ID</th>
                                <th scope="col">Title</th>
                                <th scope="col">Company</th>
                                <th class="d-flex justify-content-end" scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(drive,index) in drivesList" :key="drive.drive_id">
                                <td>{{ index+1 }}</td>
                                <td>Drive {{ drive.drive_id }}</td>
                                <td>{{ drive.title }}</td>
                                <td>{{ drive.company_name }}</td>
                                <td class="d-flex justify-content-end"><button class="btn btn-outline-primary btn-sm"
                                        @click="viewDrive(drive.drive_id)">View Drive</button>
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
        name: 'DriveSearch',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                isLoading: true,
                drivesList: []
            }
        },
        methods: {
            async fetchFilteredDrives(filters) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-searched-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        },
                        params: filters
                    });
                    this.drivesList = res.data.drives
                    console.log(res.data.drives)
                } catch (error) {
                    console.error("Failed to fetch filtered drives");
                    this.drivesList = [];
                } finally {
                    this.isLoading = false;
                }
            },

            async fetchEligibleDrives() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-eligible-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    this.drivesList = res.data.drives
                } catch (error) {
                    console.error("Failed to fetch eligible drives");
                    this.drivesList = [];
                } finally {
                    this.isLoading = false;
                }
            },

            async fetchAllDrives() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-ongoing-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    this.drivesList = res.data.ongoingDrives
                } catch (error) {
                    console.error("Failed to fetch all drives");
                    this.drivesList = [];
                } finally {
                    this.isLoading = false;
                }
            },

            viewDrive(driveId) {
                if (this.role === 'admin') {
                    this.$router.push({
                        name: "admin-drive-details",
                        params: {
                            driveId: driveId
                        }
                    });
                } else {
                    this.$router.push({
                        name: "student-drive-details",
                        params: {
                            driveId: driveId
                        }
                    });
                }
            }
        },
        async mounted() {
            const queryParams = this.$route.query;

            if (queryParams.type === 'eligible') {
                await this.fetchEligibleDrives();
            } else if (Object.keys(queryParams).length > 0) {
                await this.fetchFilteredDrives(queryParams);
            } else {
                await this.fetchAllDrives();
            }
        }
    }
</script>