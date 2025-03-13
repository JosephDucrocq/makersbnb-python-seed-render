document.addEventListener('DOMContentLoaded', function () {
    // Get price from the global spaceData object
    const pricePerNight = parseFloat(window.spaceData.price);
    const serviceFeeRate = 0.12; // 12% service fee

    // Use availability data from space
    const availabilityData = window.spaceData.availabilityData || {};

    let currentDate = new Date();
    let selectedStartDate = null;
    let selectedEndDate = null;

    // DOM Elements
    const calendarGrid = document.querySelector('.calendar-grid');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevButton = document.getElementById('prevMonth');
    const nextButton = document.getElementById('nextMonth');
    const checkInDateElement = document.getElementById('check-in-date');
    const checkOutDateElement = document.getElementById('check-out-date');
    const nightsCountElement = document.getElementById('nights-count');
    const priceNightsElement = document.getElementById('price-nights');
    const subtotalElement = document.getElementById('subtotal');
    const serviceFeeElement = document.getElementById('service-fee');
    const totalPriceElement = document.getElementById('total-price');
    const confirmButton = document.getElementById('confirm-booking');

    // Initialize calendar
    renderCalendar();

    // Event listeners
    prevButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    document.getElementById('booking-form').addEventListener('submit', function (event) {
        // Update form fields before submission
        updateFormFields();
    });

    // Calendar rendering function
    function renderCalendar() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        // Update month/year display
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'];
        currentMonthElement.textContent = `${monthNames[month]} ${year}`;

        // Clear existing calendar days (except headers)
        const dayElements = document.querySelectorAll('.calendar-day');
        dayElements.forEach(day => day.remove());

        // Get first day of month and total days in month
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const totalDays = lastDay.getDate();

        // Get the day of week the first day falls on (0 = Sunday, 6 = Saturday)
        const firstDayOfWeek = firstDay.getDay();

        // Get some days from previous month to fill the first row
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        for (let i = 0; i < firstDayOfWeek; i++) {
            const dayNum = prevMonthLastDay - firstDayOfWeek + i + 1;
            const dayElement = createDayElement(dayNum, true, false);
            dayElement.classList.add('other-month');
            calendarGrid.appendChild(dayElement);
        }

        // Add current month days
        for (let day = 1; day <= totalDays; day++) {
            const date = new Date(year, month, day);
            const dateString = formatDate(date);

            // Check if this date is available
            // A date is available only if it is in the availability dictionary AND its value is true
            // If it's not in the dictionary or its value is false, it's unavailable
            const isAvailable = dateString in availabilityData && availabilityData[dateString] === true;

            const dayElement = createDayElement(day, false, isAvailable);

            // Check if this is a selected date
            if (selectedStartDate && selectedEndDate) {
                const currentDate = new Date(year, month, day);
                if (currentDate >= selectedStartDate && currentDate <= selectedEndDate) {
                    dayElement.classList.add('selected');
                }
            } else if (selectedStartDate) {
                const currentDate = new Date(year, month, day);
                if (currentDate.getTime() === selectedStartDate.getTime()) {
                    dayElement.classList.add('selected');
                }
            }

            // Add click handler for day selection
            if (isAvailable) {
                dayElement.addEventListener('click', () => {
                    const clickedDate = new Date(year, month, day);

                    if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
                        // New selection
                        selectedStartDate = clickedDate;
                        selectedEndDate = null;
                        updateBookingSummary();
                        renderCalendar(); // Re-render to show selection
                    } else {
                        // Adding end date to existing selection
                        if (clickedDate < selectedStartDate) {
                            // If clicked before start date, swap them
                            selectedEndDate = selectedStartDate;
                            selectedStartDate = clickedDate;
                        } else {
                            selectedEndDate = clickedDate;
                        }
                        updateBookingSummary();
                        renderCalendar(); // Re-render to show selection
                    }
                });
            }

            calendarGrid.appendChild(dayElement);
        }

        // Fill remaining grid spaces with next month's days
        const totalCells = 42; // 6 rows of 7 days
        const remainingCells = totalCells - (firstDayOfWeek + totalDays);

        for (let day = 1; day <= remainingCells; day++) {
            const dayElement = createDayElement(day, true, false);
            dayElement.classList.add('other-month');
            calendarGrid.appendChild(dayElement);
        }
    }

    // Helper function to create a day element
    function createDayElement(day, isOtherMonth, isAvailable) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';

        if (!isOtherMonth) {
            dayElement.classList.add(isAvailable ? 'available' : 'unavailable');
        }

        const dayNumber = document.createElement('div');
        dayNumber.className = 'calendar-day-number';
        dayNumber.textContent = day;
        dayElement.appendChild(dayNumber);

        if (!isOtherMonth && isAvailable) {
            const price = document.createElement('div');
            price.className = 'calendar-day-price';
            price.textContent = `£${pricePerNight}`;
            dayElement.appendChild(price);
        }

        return dayElement;
    }

    // Format date as YYYY-MM-DD
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // Update booking summary based on selected dates
    function updateBookingSummary() {
        if (selectedStartDate) {
            checkInDateElement.textContent = formatDateForDisplay(selectedStartDate);

            if (selectedEndDate) {
                checkOutDateElement.textContent = formatDateForDisplay(selectedEndDate);

                // Check if all dates in range are available
                let allDatesAvailable = true;
                let currentCheckDate = new Date(selectedStartDate);

                while (currentCheckDate <= selectedEndDate) {
                    const dateString = formatDate(currentCheckDate);
                    if (!(dateString in availabilityData && availabilityData[dateString] === true)) {
                        allDatesAvailable = false;
                        break;
                    }
                    // Move to next day
                    currentCheckDate.setDate(currentCheckDate.getDate() + 1);
                }

                if (!allDatesAvailable) {
                    // Display warning that not all dates are available
                    checkOutDateElement.textContent = 'Date range includes unavailable dates';
                    nightsCountElement.textContent = '0';
                    priceNightsElement.textContent = '0';
                    subtotalElement.textContent = '£0';
                    serviceFeeElement.textContent = '£0';
                    totalPriceElement.textContent = '£0';
                    confirmButton.disabled = true;
                    return;
                }

                // Calculate nights
                const nights = Math.floor((selectedEndDate - selectedStartDate) / (1000 * 60 * 60 * 24));
                nightsCountElement.textContent = nights;
                priceNightsElement.textContent = nights;

                // Calculate prices
                const subtotal = nights * pricePerNight;
                const serviceFee = subtotal * serviceFeeRate;
                const total = subtotal + serviceFee;

                subtotalElement.textContent = `£${subtotal}`;
                serviceFeeElement.textContent = `£${serviceFee.toFixed(2)}`;
                totalPriceElement.textContent = `£${total.toFixed(2)}`;

                // Enable confirm button
                confirmButton.disabled = false;

                // Update hidden form fields
                updateFormFields();
            } else {
                checkOutDateElement.textContent = 'Select a date';
                nightsCountElement.textContent = '0';
                priceNightsElement.textContent = '0';
                subtotalElement.textContent = '£0';
                serviceFeeElement.textContent = '£0';
                totalPriceElement.textContent = '£0';
                confirmButton.disabled = true;
            }
        } else {
            checkInDateElement.textContent = 'Select a date';
            checkOutDateElement.textContent = 'Select a date';
            nightsCountElement.textContent = '0';
            priceNightsElement.textContent = '0';
            subtotalElement.textContent = '£0';
            serviceFeeElement.textContent = '£0';
            totalPriceElement.textContent = '£0';
            confirmButton.disabled = true;
        }
    }

    // Format date for display (e.g., "Mon, Mar 15, 2025")
    function formatDateForDisplay(date) {
        const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }

    // Update form fields with current values
    function updateFormFields() {
        if (selectedStartDate && selectedEndDate) {
            document.getElementById('form-check-in').value = formatDate(selectedStartDate);
            document.getElementById('form-check-out').value = formatDate(selectedEndDate);

            const nights = Math.floor((selectedEndDate - selectedStartDate) / (1000 * 60 * 60 * 24));
            document.getElementById('form-nights').value = nights;

            const subtotal = nights * pricePerNight;
            const serviceFee = subtotal * serviceFeeRate;
            const total = subtotal + serviceFee;

            document.getElementById('form-total-price').value = total.toFixed(2);
        }
    }
});