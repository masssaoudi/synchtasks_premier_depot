<template>
  <div class="segment-task-form">
    <div class="form-header">
      <h3>Créer une nouvelle tâche</h3>
      <div v-if="currentSegment" class="segment-indicator">
        <span class="segment-icon">{{ currentSegment.icon }}</span>
        <span class="segment-name">{{ currentSegment.name }}</span>
      </div>
    </div>

    <form class="task-form" @submit.prevent="submitTask">
      <div class="form-group">
        <label for="title">Titre de la tâche</label>
        <input
          id="title"
          v-model="taskData.title"
          type="text"
          placeholder="Entrez le titre de la tâche"
          class="form-input"
          required
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="taskData.description"
          placeholder="Décrivez votre tâche"
          class="form-textarea"
          rows="3"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="category">Catégorie</label>
          <select
            id="category"
            v-model="taskData.category"
            class="form-select"
            required
          >
            <option value="">Sélectionnez une catégorie</option>
            <option
              v-for="category in segmentCategories"
              :key="category"
              :value="category"
            >
              {{ category }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="priority">Priorité</label>
          <select
            id="priority"
            v-model="taskData.priority"
            class="form-select"
            required
          >
            <option value="">Sélectionnez une priorité</option>
            <option
              v-for="priority in segmentPriorities"
              :key="priority"
              :value="priority"
            >
              {{ priority }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="dueDate">Date d'échéance</label>
        <input
          id="dueDate"
          v-model="taskData.due_date"
          type="datetime-local"
          class="form-input"
        />
      </div>

      <div class="form-actions">
        <button
          type="button"
          class="btn btn-secondary"
          @click="$emit('cancel')"
        >
          Annuler
        </button>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Création...' : 'Créer la tâche' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
  import { ref, computed } from 'vue';
  import { useSegmentsStore } from '../stores/segments';
  import { useTasksStore } from '../stores/tasks';

  const emit = defineEmits(['cancel', 'created']);

  const segmentsStore = useSegmentsStore();
  const tasksStore = useTasksStore();

  const loading = ref(false);
  const taskData = ref({
    title: '',
    description: '',
    category: '',
    priority: '',
    due_date: '',
    status: 'À faire',
  });

  // Computed properties
  const currentSegment = computed(() => segmentsStore.currentSegment);
  const segmentCategories = computed(() => tasksStore.segmentCategories);
  const segmentPriorities = computed(() => tasksStore.segmentPriorities);

  const submitTask = async () => {
    loading.value = true;

    try {
      const result = await tasksStore.createTask(taskData.value);

      if (result.success) {
        // Réinitialiser le formulaire
        taskData.value = {
          title: '',
          description: '',
          category: '',
          priority: '',
          due_date: '',
          status: 'À faire',
        };

        emit('created', result.task);
      }
    } catch (error) {
      console.error('Erreur lors de la création de la tâche:', error);
    } finally {
      loading.value = false;
    }
  };
</script>

<style scoped>
  .segment-task-form {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #f0f0f0;
  }

  .form-header h3 {
    margin: 0;
    color: #333;
    font-size: 1.5rem;
  }

  .segment-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f8f9fa;
    border-radius: 20px;
    border: 2px solid var(--segment-color, #007bff);
  }

  .segment-icon {
    font-size: 1.2rem;
  }

  .segment-name {
    font-weight: 500;
    color: #333;
  }

  .task-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  label {
    font-weight: 500;
    color: #333;
    font-size: 0.9rem;
  }

  .form-input,
  .form-textarea,
  .form-select {
    padding: 0.8rem;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
  }

  .form-input:focus,
  .form-textarea:focus,
  .form-select:focus {
    outline: none;
    border-color: var(--segment-color, #007bff);
  }

  .form-textarea {
    resize: vertical;
    min-height: 80px;
  }

  .form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1rem;
    padding-top: 1.5rem;
    border-top: 2px solid #f0f0f0;
  }

  .btn {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
  }

  .btn-primary {
    background: var(--segment-color, #007bff);
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }

  .btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-secondary {
    background: #f8f9fa;
    color: #666;
    border: 2px solid #e9ecef;
  }

  .btn-secondary:hover {
    background: #e9ecef;
    color: #333;
  }

  @media (max-width: 768px) {
    .segment-task-form {
      padding: 1.5rem;
    }

    .form-header {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start;
    }

    .form-row {
      grid-template-columns: 1fr;
    }

    .form-actions {
      flex-direction: column;
    }
  }
</style>
