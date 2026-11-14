const KEY = 'focalpoint_incident_queue'

export function getQueue(): any[] {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '[]')
  } catch {
    return []
  }
}

export function addToQueue(item: any) {
  const q = getQueue()
  q.push({ ...item, queuedAt: new Date().toISOString() })
  localStorage.setItem(KEY, JSON.stringify(q))
}

export function clearQueue() {
  localStorage.removeItem(KEY)
}
