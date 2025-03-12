document.addEventListener('DOMContentLoaded', function () {
    // Get space data from the global spaceData object set in the HTML
    const pricePerNight = parseFloat(window.spaceData.price);
    const serviceFeeRate = 0.12; // 12% service fee

    // Get availability data from the window.spaceData.availabilityData object
    // In a real app, this would be the dates_available_dict from the Space object
    const availabilityData = window.spaceData.availabilityData || {};

    // Initialize calendar state
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

    // Form hidden fields
    const formCheckIn = document.getElementById('form-check-in');
    const formCheckOut = document.getElementById('form-check-out');
    const formNights = document.getElementById('form-nights');
    const formTotalPrice = document.getElementById('form-total-price');

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

            // Check if this date is available - only if the date is in the availability dict
            // and the value is true, and the date is not in the past
            const isPastDate = date < new Date(new Date().setHours(0, 0, 0, 0));
            const isAvailable = !isPastDate && availabilityData[dateString] === true;

            const dayElement = createDayElement(day, false, isAvailable);

            // Check if this is a selected date or in range
            if (selectedStartDate && selectedEndDate) {
                const currentDate = new Date(year, month, day);
                if (isSameDay(currentDate, selectedStartDate) || isSameDay(currentDate, selectedEndDate)) {
                    dayElement.classList.add('selected');
                } else if (currentDate > selectedStartDate && currentDate < selectedEndDate) {
                    dayElement.classList.add('in-range');
                }
            } else if (selectedStartDate) {
                const currentDate = new Date(year, month, day);
                if (isSameDay(currentDate, selectedStartDate)) {
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

    // Check if two dates are the same day
    function isSameDay(date1, date2) {
        return date1.getFullYear() === date2.getFullYear() &&
            date1.getMonth() === date2.getMonth() &&
            date1.getDate() === date2.getDate();
    }

    // Update booking summary based on selected dates
    function updateBookingSummary() {
        if (selectedStartDate) {
            checkInDateElement.textContent = formatDateForDisplay(selectedStartDate);
            formCheckIn.value = formatDate(selectedStartDate);

            if (selectedEndDate) {
                checkOutDateElement.textContent = formatDateForDisplay(selectedEndDate);
                formCheckOut.value = formatDate(selectedEndDate);

                // Calculate nights
                const nights = Math.floor((selectedEndDate - selectedStartDate) / (1000 * 60 * 60 * 24));
                nightsCountElement.textContent = nights;
                priceNightsElement.textContent = nights;
                formNights.value = nights;

                // Calculate prices
                const subtotal = nights * pricePerNight;
                const serviceFee = subtotal * serviceFeeRate;
                const total = subtotal + serviceFee;

                subtotalElement.textContent = `£${subtotal.toFixed(2)}`;
                serviceFeeElement.textContent = `£${serviceFee.toFixed(2)}`;
                totalPriceElement.textContent = `£${total.toFixed(2)}`;
                formTotalPrice.value = total.toFixed(2);

                // Enable confirm button
                confirmButton.disabled = false;
            } else {
                checkOutDateElement.textContent = 'Select a date';
                formCheckOut.value = '';
                resetPriceDisplay();
            }
        } else {
            checkInDateElement.textContent = 'Select a date';
            formCheckIn.value = '';
            checkOutDateElement.textContent = 'Select a date';
            formCheckOut.value = '';
            resetPriceDisplay();
        }
    }

    function resetPriceDisplay() {
        nightsCountElement.textContent = '0';
        priceNightsElement.textContent = '0';
        subtotalElement.textContent = '£0';
        serviceFeeElement.textContent = '£0';
        totalPriceElement.textContent = '£0';
        formNights.value = '0';
        formTotalPrice.value = '0';
        confirmButton.disabled = true;
    }

    // Format date for display (e.g., "Mon, Mar 15, 2025")
    function formatDateForDisplay(date) {
        const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }
});
