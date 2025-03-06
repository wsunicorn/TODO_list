document.addEventListener('DOMContentLoaded', () => {
    // Ẩn checkbox và nút hành động ban đầu
    document.querySelectorAll('.task-checkbox').forEach(cb => {
        cb.style.display = 'none';
    });
    document.getElementById('deleteActions').style.display = 'none';

    const todoList = document.querySelector('.todo-list');
    const noTasksMessage = document.getElementById('noTasksMessage');

    function showTemporaryMessage(message) {
        noTasksMessage.textContent = message;
        noTasksMessage.style.display = 'block';
        setTimeout(() => {
            noTasksMessage.style.display = 'none';
        }, 5000); // Ẩn sau 5 giây (5000ms)
    }

    function showCheckboxesAndButtons() {
        // Kiểm tra nếu không có task
        if (todoList.children.length === 0) {
            showTemporaryMessage('Không có gì để xóa.');
            return; // Không làm gì thêm nếu danh sách trống
        }

        // Chỉ thực hiện nếu có task
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

    function showConfirmModal(message) {
        document.getElementById('confirmMessage').textContent = message;
        document.getElementById('confirmModal').style.display = 'block';
    }

    function hideConfirmModal() {
        document.getElementById('confirmModal').style.display = 'none';
    }

    function confirmDelete(taskIds) {
        fetch('/delete_multiple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_ids: taskIds })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text || "Có lỗi xảy ra"); });
            }
            return response.text();
        })
        .then(() => {
            if (taskIds === "all") {
                window.location.reload(); // Reload trang để cập nhật toàn bộ
            } else {
                taskIds.forEach(id => {
                    let row = document.querySelector(`input[value="${id}"]`).closest('li');
                    if (row) row.remove();
                });
                if (todoList.children.length === 0) {
                    showTemporaryMessage('Không có gì để xóa.');
                }
            }
            hideConfirmModal();
            hideCheckboxesAndButtons();
        })
        .catch(error => {
            alert("Lỗi: " + error.message);
        });
    }

    function deleteSelected() {
        let selectedIds = Array.from(document.querySelectorAll('input.task-checkbox:checked'))
                              .map(cb => cb.value);
        if (selectedIds.length === 0) {
            alert("Vui lòng chọn ít nhất một task để xóa.");
            return;
        }
        showConfirmModal("Bạn muốn thực hiện xóa những gì mình đã chọn?");
        document.querySelector('#confirmModal .delete-btn').onclick = () => confirmDelete(selectedIds);
    }

    function deleteAll() {
        const allTasks = document.querySelectorAll('input.task-checkbox');
        if (allTasks.length === 0) {
            alert("Không có task nào để xóa.");
            return;
        }
        showConfirmModal("Bạn muốn xóa tất cả các task?");
        document.querySelector('#confirmModal .delete-btn').onclick = () => confirmDelete("all");
    }

    // Gắn sự kiện cho nút "Xóa Nhiều"
    document.getElementById('deleteMultipleBtn').addEventListener('click', showCheckboxesAndButtons);

    // Gắn sự kiện cho checkbox
    document.querySelectorAll('.task-checkbox').forEach(cb => {
        cb.addEventListener('change', showDeleteSelectedButton);
    });

    // Gắn sự kiện cho các nút trong deleteActions
    document.getElementById('deleteSelectedBtn')?.addEventListener('click', deleteSelected);
    document.getElementById('deleteAllBtn')?.addEventListener('click', deleteAll);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', hideCheckboxesAndButtons);

    // Gắn sự kiện cho nút Hủy trong modal
    document.querySelector('#confirmModal .add-btn')?.addEventListener('click', hideConfirmModal);
});