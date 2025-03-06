document.addEventListener('DOMContentLoaded', () => {
    // Ẩn checkbox và nút hành động ban đầu
    document.querySelectorAll('.task-checkbox').forEach(cb => {
        cb.style.display = 'none';
    });
    document.getElementById('deleteActions').style.display = 'none';

    function showCheckboxesAndButtons() {
        document.getElementById('deleteMultipleBtn').style.display = 'none'; // Ẩn nút "Xóa Nhiều"
        document.querySelectorAll('.task-checkbox').forEach(cb => {
            cb.style.display = 'inline';
        });
        document.getElementById('deleteActions').style.display = 'flex';
        showDeleteSelectedButton();
    }

    function hideCheckboxesAndButtons() {
        document.getElementById('deleteMultipleBtn').style.display = 'inline-block'; // Hiện lại nút "Xóa Nhiều"
        document.querySelectorAll('.task-checkbox').forEach(cb => {
            cb.style.display = 'none';
            cb.checked = false; // Bỏ chọn tất cả checkbox
        });
        document.getElementById('deleteActions').style.display = 'none';
    }

    function showDeleteSelectedButton() {
        let selected = document.querySelectorAll('input.task-checkbox:checked').length > 0;
        document.getElementById('deleteSelectedBtn').style.display = selected ? 'inline-block' : 'none';
    }

    function showConfirmModal() {
        document.getElementById('confirmModal').style.display = 'block';
    }

    function hideConfirmModal() {
        document.getElementById('confirmModal').style.display = 'none';
    }

    function confirmDelete() {
        let selectedIds = Array.from(document.querySelectorAll('input.task-checkbox:checked'))
                              .map(cb => cb.value);
        if (selectedIds.length === 0) {
            alert("Vui lòng chọn ít nhất một task để xóa.");
            return;
        }

        fetch('/delete_multiple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_ids: selectedIds })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text || "Có lỗi xảy ra"); });
            }
            return response.text();
        })
        .then(() => {
            selectedIds.forEach(id => {
                let row = document.querySelector(`input[value="${id}"]`).closest('li');
                row.remove();
            });
            hideConfirmModal();
            hideCheckboxesAndButtons();
        })
        .catch(error => {
            alert("Lỗi: " + error.message);
        });
    }

    // Gắn sự kiện cho nút "Xóa Nhiều"
    document.getElementById('deleteMultipleBtn').addEventListener('click', showCheckboxesAndButtons);

    // Gắn sự kiện cho checkbox
    document.querySelectorAll('.task-checkbox').forEach(cb => {
        cb.addEventListener('change', showDeleteSelectedButton);
    });

    // Gắn sự kiện cho các nút trong deleteActions
    document.getElementById('deleteSelectedBtn')?.addEventListener('click', showConfirmModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', hideCheckboxesAndButtons);

    // Gắn sự kiện cho các nút trong modal
    document.querySelector('#confirmModal .delete-btn')?.addEventListener('click', confirmDelete);
    document.querySelector('#confirmModal .add-btn')?.addEventListener('click', hideConfirmModal);
});