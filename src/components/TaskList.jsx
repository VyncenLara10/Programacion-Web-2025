import TaskItem from "./TaskItem";

function TaskList({ tasks }) {
  return (
    <ul>
      {tasks.map((t) => (
        <TaskItem key={t.id} task={t} />
      ))}
    </ul>
  );
}

export default TaskList;
