// Edit Modal logic
const modal = document.getElementById('editModal');
const editBtn = document.querySelectorAll('.edit-btn');
editBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        document.getElementById('edit-id').value = btn.dataset.id;
        document.getElementById('edit-name').value = btn.dataset.name;
        document.getElementById('edit-phone').value = btn.dataset.phone;
        document.getElementById('edit-email').value = btn.dataset.email;
        modal.classList.remove('hidden');
    });
});

function closeModal() {
    modal.classList.add('hidden');
}

modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});