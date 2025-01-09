import React, { useState } from 'react';
import {
    TextField,
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { tr } from 'date-fns/locale';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

export default function Profitability() {
    const [formData, setFormData] = useState({
        // clientName: 'geetika',
        dateStart: new Date(),
        dateEnd: new Date(),
        // countryName: ['All Countries'],
        channelName: ['All Channels']
    });

    const [adsenseData, setAdsenseData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [view, setView] = useState(true);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };
    

    const handleChange = (event, newAlignment) => {
        setView(newAlignment);
    };

    const handleDateChange = (field, date) => {
        setFormData((prev) => ({
            ...prev,
            [field]: date,
        }));
    };

    const handleChannelChange = (e) => {
        const channels = e.target.value.split(',').map((channel) => channel.trim());
        setFormData((prev) => ({
            ...prev,
            channelName: channels,
        }));
    };

    const handleSearch = async () => {
        setLoading(true);
        setError(null);
        try {
            const payload = {
                channelName: formData.channelName.length === 1 && formData.channelName[0] === "" ? 'All Channels' : formData.channelName,
                dateStart: formData.dateStart.toISOString().split('T')[0],
                dateEnd: formData.dateEnd.toISOString().split('T')[0],
                viewMode: view
            };

            console.log('Payload being sent to API:', payload);

            const response = await fetch('http://localhost:5000/ads-earning', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('API Response:', data);
            setAdsenseData(data);


        } catch (err) {
            console.error('Error fetching data:', err);
            setError(`Failed to fetch AdSense data: ${err.message}`);
            setAdsenseData([]);
        }
        setLoading(false);
    };

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns}>
            <div className="p-6 bg-gray-100 min-h-screen">
                <div className="bg-white shadow-md rounded-lg p-6">
                    <h1 className="text-2xl font-bold mb-6">AdSense Profitability</h1>

                    <div className="grid grid-cols-2 gap-4 mb-6">
                        {/* <TextField
                            label="Client Name"
                            name="clientName"
                            value={formData.clientName}
                            onChange={handleInputChange}
                            variant="outlined"
                            fullWidth
                        /> */}

                        <DatePicker
                            label="Date Start"
                            value={formData.dateStart}
                            onChange={(date) => handleDateChange('dateStart', date)}
                            renderInput={(params) => <TextField {...params} fullWidth />}
                        />

                        <DatePicker
                            label="Date End"
                            value={formData.dateEnd}
                            onChange={(date) => handleDateChange('dateEnd', date)}
                            renderInput={(params) => <TextField {...params} fullWidth />}
                        />

                        <TextField
                            label="Channels (comma-separated)"
                            value={formData.channelName.join(', ')}
                            onChange={handleChannelChange}
                            variant="outlined"
                            fullWidth
                        />
                        <ToggleButtonGroup
                            color="primary"
                            value={view}
                            exclusive
                            onChange={handleChange}
                            aria-label="Platform"
                        >
                            <ToggleButton value={false}>Regular</ToggleButton>
                            <ToggleButton value={true}>Geowise</ToggleButton>
                        </ToggleButtonGroup>
                    </div>

                    <Button
                        variant="contained"
                        onClick={handleSearch}
                        disabled={loading}
                        color="primary"
                    >
                        {loading ? 'Searching...' : 'Search'}
                    </Button>

                    {error && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4">
                            {error}
                        </div>
                    )}

                    {adsenseData.length > 0 && (
                        <TableContainer component={Paper} className="mt-6">
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Date</TableCell>
                                        <TableCell>Channel Name</TableCell>
                                        <TableCell>Country Name</TableCell>
                                        {/* <TableCell>Channel ID</TableCell> */}
                                        <TableCell>Estimated Earnings (INR)</TableCell>
                                        {/* <TableCell>Page Views</TableCell> */}
                                        {/* <TableCell>Impressions</TableCell> */}
                                        {/* <TableCell>CTR (%)</TableCell>
                                        <TableCell>Clicks</TableCell>
                                        <TableCell>CPC (INR)</TableCell> */}
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {adsenseData.map((item, index) => (
                                        <TableRow key={index}>
                                            <TableCell>{item.date ?? 'N/A'}</TableCell>
                                            <TableCell>{item.channelName ?? 'N/A'}</TableCell>
                                            <TableCell>{item.countryName ?? 'N/A'}</TableCell>
                                            {/* <TableCell>{item.channelId ?? 'N/A'}</TableCell> */}
                                            <TableCell>{item.rev ?? 'N/A'}</TableCell>
                                            {/* <TableCell>{item.pv ?? 'N/A'}</TableCell> */}
                                            {/* <TableCell>{item.imp ?? 'N/A'}</TableCell> */}
                                            {/* <TableCell>{item.impCTR ?? 'N/A'}</TableCell>
                                            <TableCell>{item.clicks ?? 'N/A'}</TableCell>
                                            <TableCell>{item.cpc ?? 'N/A'}</TableCell> */}
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    )}

                    {adsenseData.length === 0 && !loading && !error && (
                        <p className="text-gray-500 mt-4">No data available.</p>
                    )}
                </div>
            </div>
        </LocalizationProvider>
    );
}
