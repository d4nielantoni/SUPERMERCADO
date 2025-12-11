document.addEventListener('DOMContentLoaded', function() {
    initializeCollapseBehavior();
    initializePhotoModal();
});

function initializeCollapseBehavior() {
    const toggleBtnMobile = document.querySelector('.toggle-btn-mobile');
    const toggleBtnDesktop = document.querySelector('.toggle-btn-desktop');
    const addItemForm = document.getElementById('addItemForm');

    if (toggleBtnMobile && addItemForm) {
        addItemForm.addEventListener('show.bs.collapse', function() {
            toggleBtnMobile.setAttribute('aria-expanded', 'true');
            if (toggleBtnDesktop) {
                toggleBtnDesktop.setAttribute('aria-expanded', 'true');
            }
        });

        addItemForm.addEventListener('hide.bs.collapse', function() {
            toggleBtnMobile.setAttribute('aria-expanded', 'false');
            if (toggleBtnDesktop) {
                toggleBtnDesktop.setAttribute('aria-expanded', 'false');
            }
        });
    }

    if (typeof jQuery !== 'undefined') {
        initializeFormValidation();
    }
}

function initializePhotoModal() {
    window.expandPhoto = function(photoUrl, itemName) {
        const expandedPhoto = document.getElementById('expandedPhoto');
        const photoModalLabel = document.getElementById('photoModalLabel');

        if (expandedPhoto && photoModalLabel) {
            expandedPhoto.src = photoUrl;
            expandedPhoto.alt = itemName;
            photoModalLabel.textContent = itemName;
        }
    };
}

function initializeFormValidation() {
    validateQuantityField();
    validatePriceField();
}

function validateQuantityField() {
    $('#id_quantity')
        .on('keypress', function(e) {
            if (!/[0-9]/.test(String.fromCharCode(e.which))) {
                e.preventDefault();
            }
        })
        .on('paste', function(e) {
            const pastedData = e.originalEvent.clipboardData.getData('text');
            if (!/^\d+$/.test(pastedData)) {
                e.preventDefault();
            }
        })
        .on('input', function() {
            this.value = this.value.replace(/[^\d]/g, '');
        });
}

function validatePriceField() {
    $('#id_price')
        .on('keypress', function(e) {
            const char = String.fromCharCode(e.which);
            const value = $(this).val();
            if (!/[0-9.]/.test(char) || (char === '.' && value.includes('.'))) {
                e.preventDefault();
            }
        })
        .on('paste', function(e) {
            const pastedData = e.originalEvent.clipboardData.getData('text');
            if (!/^[\d.]+$/.test(pastedData)) {
                e.preventDefault();
            }
        })
        .on('input', function() {
            let value = this.value.replace(/[^\d.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            this.value = value;
        });
}
