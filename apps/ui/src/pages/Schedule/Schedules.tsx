import { useCreateScheduleService } from 'services/schedule/useCreateScheduleService'

const Schedules = () => {
  const [createScheduleService] = useCreateScheduleService()

  return <button onClick={() => createScheduleService('dad')}>schedule page</button>
}

export default Schedules
