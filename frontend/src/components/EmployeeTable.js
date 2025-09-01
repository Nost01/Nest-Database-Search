export default function EmployeeTable({ employees }) {
    if (!employees.length) return <p>No employees found.</p>;
 
    return (
        <table border="1" cellPadding="5" cellSpacing="0">
            <thead>
                <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Department</th>
                    <th>Vehicle Plate</th>
                    <th>Vehicle Description</th>
                    <th>Vehicle Colour</th>
                    <th>Vehicle Make</th>
                    <th>Vehicle Model</th>
                    <th>Stall Number</th>
                    <th>Number of Vehicles</th>
                    <th>Phone Number</th>
                </tr>
            </thead>
            <tbody>
                {employees.map((e, i) => (
                    <tr key={i}>
                        <td>{e.FirstName}</td>
                        <td>{e.LastName}</td>
                        <td>{e.Department}</td>
                        <td>{e.VehiclePlate}</td>
                        <td>{e.VehicleDescription}</td>
                        <td>{e.VehicleColour}</td>
                        <td>{e.VehicleMake}</td>
                        <td>{e.VehicleModel}</td>
                        <td>{e.StallNumber}</td>
                        <td>{e.NumberOfVehicles}</td>
                        <td>{e.PhoneNumber}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}