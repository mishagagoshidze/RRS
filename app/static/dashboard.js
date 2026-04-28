
function showSection(sectionId) {
    // 1. ვიპოვოთ ყველა სექცია, რომელსაც აქვს 'content-section' კლასი
    const sections = document.querySelectorAll('.content-section');
    
    // 2. ყველა სექციას დავადოთ 'hidden' კლასი (დავმალოთ ყველაფერი)
    sections.forEach(section => {
        section.classList.add('hidden');
    });

    // 3. მხოლოდ იმ სექციას მოვხსნათ 'hidden', რომელიც გვჭირდება
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.remove('hidden');
    }

}

// <--- USER

function User_Add() {
    
    const form = document.getElementById('form-main-user');
    if(form) form.reset();
    
    //const emailField = document.getElementById('form-user-email-field-container');
    //if(emailField) emailField.classList.remove('hidden');
    
    document.getElementById('form-user-title').innerText = "ახალი მომხმარებლის დამატება";
    
    document.getElementById('form-user-submit-btn').innerText = "მომხმარებლის შექმნა";
    
    document.getElementById('form-user-id').value = "";

    document.getElementById('form-user-super-admin').checked = false;
    document.getElementById('form-user-is-active').checked = false;
    
    showSection('form-user');

} 

function User_Edit(id, email, fname, lname, phone, is_active, super_admin, type) {
      
    if (type == 1 || String(type) == '1'){
        document.getElementById('form-user-email-field-container').classList.add('hidden');
        document.getElementById('form-user-admin-controls').classList.add('hidden');
    }else{
        document.getElementById('form-user-email-field-container').classList.remove('hidden');
        document.getElementById('form-user-admin-controls').classList.remove('hidden');
    }

    document.getElementById('form-user-title').innerText = "მომხმარებლის რედაქტირება";
    
    document.getElementById('form-user-submit-btn').innerText = "განახლება";
    
    document.getElementById('form-user-id').value = id;    
    
    document.getElementById('form-user-email').value = email;    
    
    document.getElementById('form-user-first-name').value = fname;    
    
    document.getElementById('form-user-last-name').value = lname;
    
    document.getElementById('form-user-telephone').value = phone;
    
    // ფუნქცია მნიშვნელობის ბულეანად გადასაქცევად
    const toBool = (val) => val === true || val === 'True' || val === 'true' || val === 1 || val === '1';

    const activeCheckbox = document.getElementById('form-user-is-active');
    if (activeCheckbox) {
        activeCheckbox.checked = toBool(is_active);
    }

    const superadminCheckbox = document.getElementById('form-user-super-admin');
    if (superadminCheckbox) {
        superadminCheckbox.checked = toBool(super_admin);
    }
    
    showSection('form-user');

}

// USER ---> 


// <--- ROOM

function Room_Add() {
    
    const form = document.getElementById('form-main-user');
    if(form) form.reset();
    
    document.getElementById('form-room-title').innerText = "ახალი ოთახის დამატება";
    
    document.getElementById('form-room-submit-btn').innerHTML = '<i class="fas fa-plus mr-2"></i> ოთახის შექმნა';
    
    document.getElementById('form-room-id').value = ""; 
    
    showSection('form-room');

}

function Room_Edit(id, number, floor, description, admin_id) { 
    
    const id_room = document.getElementById('form-room-id');
    if (id_room) {
        id_room.value = id;
    }

    const adminSelect = document.getElementById('form-room-user-id');
    if (adminSelect) {        
        adminSelect.value = admin_id ? admin_id : ""; 
    }

    document.getElementById('form-room-title').innerText = "ოთახის რედაქტირება";
    
    document.getElementById('form-room-submit-btn').innerHTML = '<i class="fas fa-save mr-2"></i> ცვლილებების შენახვა';
    
    document.getElementById('form-room-id').value = id;
    
    document.getElementById('form-room-number').value = number;
    
    document.getElementById('form-room-floor').value = floor;
    
    document.getElementById('form-room-description').value = description;
    
    showSection('form-room');

}

// ROOM --->



// <--- RESERVATION

function Event_Create() {
    
    const form = document.getElementById('form-main-event');
    if(form) form.reset();
    
    showSection('form-event');

}

function Event_Create2(room_id, user_id, start_date, end_date, description) { 
    
    document.getElementById('form-event-room-id').value = room_id;
    
    document.getElementById('form-event-user-id').value = user_id;
    
    document.getElementById('form-event_start_date').value = start_date;
    
    document.getElementById('form-event_end_date').value = start_date;

    document.getElementById('form-event_end_date').value = start_date;

     document.getElementById('form-event-description').value = description;

    
    showSection('form-event');

}

// RESERVATION --->